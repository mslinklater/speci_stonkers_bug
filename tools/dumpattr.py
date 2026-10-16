import sys
from skoolkit.snapshot import Snapshot
s=Snapshot.get(sys.argv[1]); m=s.ram(-1) if hasattr(s,'ram') else None
mem=[0]*16384+list(s.ram())
for y in range(24):
    print('%2d '%y+' '.join('%02x'%mem[0x5800+y*32+x] for x in range(32)))
