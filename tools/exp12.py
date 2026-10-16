import sys; sys.path.insert(0,'.')
from fuzz2 import *
g=base(); rec=0xE4D0
place_player(g,0,976,384)
g.mem[rec+3]=0x01
setpath(g,rec,['SW']*100)
allmap=set()
for f in range(0,50*30,5):
    g.emap=set(); g.run(5); allmap|=g.emap
ex=sorted(a for a in allmap if 0xE450<=a<0xF000)
print('executed in data area:', ' '.join('%04x'%a for a in ex))
print('C9F8 executed:', 0xC9F8 in allmap, 'CB40:',0xCB40 in allmap, 'C9F1:',0xC9F1 in allmap)
