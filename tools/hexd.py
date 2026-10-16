import sys
from skoolkit.snapshot import Snapshot
s=Snapshot.get(sys.argv[1]); mem=[0]*16384+list(s.ram())
a=int(sys.argv[2],16); n=int(sys.argv[3],16); w=int(sys.argv[4]) if len(sys.argv)>4 else 16
for i in range(a,a+n,w):
    print('%04x: '%i+' '.join('%02x'%mem[j] for j in range(i,min(i+w,a+n))))
