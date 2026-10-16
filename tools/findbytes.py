import sys
from skoolkit.snapshot import Snapshot
s=Snapshot.get(sys.argv[1]); mem=bytes([0]*16384+list(s.ram()))
pat=bytes.fromhex(sys.argv[2])
i=mem.find(pat)
while i>=0:
    print(hex(i)); i=mem.find(pat,i+1)
