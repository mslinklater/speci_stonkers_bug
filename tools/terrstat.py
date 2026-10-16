import sys
from collections import Counter
from skoolkit.snapshot import Snapshot
s=Snapshot.get(sys.argv[1]); mem=[0]*16384+list(s.ram())
for band in range(3):
    c=Counter(mem[0x6000+y*160+x] for y in range(band*32,band*32+32) for x in range(160))
    print(band, ' '.join('%02x:%d'%(k,v) for k,v in sorted(c.items())))
