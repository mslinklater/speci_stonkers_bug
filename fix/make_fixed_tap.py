#!/usr/bin/env python3
"""Patch Stonkers (Imagine, 1983) to fix the infamous "bridge" crash.

Usage:
    python3 make_fixed_tap.py STONKERS.TAP STONKERS_FIXED.TAP

The input is the common TAP image of the game (the one tested had
MD5 f0c54d9f56300e177f47c62618493c2d).  The patch replaces 13 bytes at
$C9EB-$C9F7 inside the main code block (loaded at 24576/$6000) and
recalculates that block's checksum.  Nothing else on the tape changes.

What it does (see README.md for the full story):

    original                          patched
    $C9EB  JR Z,$C9F1                 $C9EB  JR Z,$C9F0
    $C9ED  INC HL                     $C9ED  INC HL
    $C9EE  JP $CA3E                   $C9EE  JR $CA3E        ; JP -> JR frees a byte
    $C9F1  LD A,(HL)                  $C9F0  LD A,(HL)
    $C9F2  SUB $01                    $C9F1  SUB $01
    $C9F4  DAA                        $C9F3  DAA
    $C9F5  LD (HL),A                  $C9F4  LD (HL),A
    $C9F6  JR NZ,$CA01                $C9F5  JR NZ,$CA01
                                      $C9F7  POP BC          ; drop the unit pointer
    $C9F8  DEC HL  (unchanged ...)    $C9F8  DEC HL  (unchanged ...)
"""
import struct
import sys

ORG = 0x6000
PATCH_ADDR = 0xC9EB
OLD = bytes([0x28, 0x04, 0x23, 0xC3, 0x3E, 0xCA, 0x7E, 0xD6, 0x01, 0x27, 0x77, 0x20, 0x09])
NEW = bytes([0x28, 0x03, 0x23, 0x18, 0x4E, 0x7E, 0xD6, 0x01, 0x27, 0x77, 0x20, 0x0A, 0xC1])


def tap_blocks(data):
    i = 0
    while i < len(data):
        length = struct.unpack('<H', data[i:i + 2])[0]
        yield i + 2, length
        i += 2 + length


def main(src, dst):
    d = bytearray(open(src, 'rb').read())
    blocks = list(tap_blocks(d))
    # The main code block: 39900 bytes of data (+flag +checksum) loaded at $6000.
    off, length = next((o, l) for o, l in blocks if l == 39902 and d[o] == 0xFF)
    p = off + 1 + (PATCH_ADDR - ORG)
    if bytes(d[p:p + len(OLD)]) == NEW:
        sys.exit('This tape is already patched.')
    if bytes(d[p:p + len(OLD)]) != OLD:
        sys.exit('Unexpected bytes at $%04X - is this a different version of Stonkers?' % PATCH_ADDR)
    d[p:p + len(NEW)] = NEW
    checksum = 0
    for b in d[off:off + length - 1]:
        checksum ^= b
    d[off + length - 1] = checksum
    open(dst, 'wb').write(d)
    print('Wrote %s (patched %d bytes at $%04X)' % (dst, sum(a != b for a, b in zip(OLD, NEW)), PATCH_ADDR))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
