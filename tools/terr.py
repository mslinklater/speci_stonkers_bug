import sys
from skoolkit.snapshot import Snapshot
s=Snapshot.get(sys.argv[1]); mem=[0]*16384+list(s.ram())
y0,y1,x0,x1=map(int,sys.argv[2:6])
print('     '+' '.join('%2d'%(x%100) for x in range(x0,x1)))
for y in range(y0,y1):
    print('%3d: '%y+' '.join('%02x'%mem[0x6000+y*160+x] for x in range(x0,x1)))
