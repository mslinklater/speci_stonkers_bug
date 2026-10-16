import sys; sys.path.insert(0,'.')
from exp import *
tests=[
 ('SW straight',(976,368),['SW']*90),
 ('SW from 121,46',(968,368),['SW']*90),
 ('NE straight from W bank',(888,456),['NE']*90),
 ('W then SW',(984,400),['W']*4+['SW']*80),
 ('S then SW',(952,360),['S']*8+['SW']*80),
 ('SW,W mix',(976,376),['SW','SW','W']*30),
]
for name,(x,y),path in tests:
    g=mkgame(x,y); rec=0xE4D0
    setpath(g,rec,path)
    r=watch(g,1500,rec,verbose=False)
    print(name, 'start',(x,y),'->', r, 'end',pos(g,rec),'flags %02x cnt %d'%(g.mem[rec],g.mem[rec+7]), flush=True)
