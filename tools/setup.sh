#!/bin/sh
# Build everything the scripts in this folder need, from YOUR copy of the tape.
#   ./setup.sh /path/to/STONKERS.TAP
# Needs python3 and (for videos) ffmpeg. Creates ./venv and ./work.
set -e
[ -n "$1" ] || { echo "usage: $0 /path/to/STONKERS.TAP"; exit 1; }
cd "$(dirname "$0")"
python3 -m venv venv
./venv/bin/pip install -q skoolkit
mkdir -p work
cp "$1" work/orig.tap
./venv/bin/python ../fix/make_fixed_tap.py work/orig.tap work/fixed.tap
# Simulated LOAD of each tape, stopping at the game's entry point (49348)
./venv/bin/tap2sna.py work/orig.tap work/stonk.z80
./venv/bin/tap2sna.py work/fixed.tap work/stonk_fixed.z80
echo
echo "Ready. Try:"
echo "  ./venv/bin/python vids2.py /tmp/crash.mp4              # the bridge crash, original game"
echo "  STONK=fixed ./venv/bin/python vids2.py /tmp/fixed.mp4  # same scene, patched game"
