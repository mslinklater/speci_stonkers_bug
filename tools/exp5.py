import sys; sys.path.insert(0,'.')
from exp3 import *
tests=[
 ('SW straight',(976,384),['SW']*90),
 ('NE from W bank',(888,456),['NE']*90),
 ('W then SW',(984,400),['W']*4+['SW']*80),
 ('SW,W mix',(976,392),['SW','SW','W']*30),
 ('W straight row50',(1000,400),['W']*120),
 ('E straight row53',(880,424),['E']*120),
]
for name,(x,y),path in tests:
    g=mkgame(x,y); rec=0xE4D0
    setview(g,13*64,6*64); g.run(20); zoom(g); g.run(60)
    setpath(g,rec,path)
    r=watch(g,1500,rec,verbose=False)
    print(name, 'start',(x,y),'->', r, 'end',pos(g,rec),'flags %02x cnt %d'%(g.mem[rec],g.mem[rec+7]), flush=True)
    g.screenshot('work/e5_%s.png'%name.replace(' ','_').replace(',','_'))
