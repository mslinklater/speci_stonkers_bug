import sys, random, json; sys.path.insert(0,'.')
from fuzz2 import *
from monitor import suspicious
from skoolkit.snapshot import Snapshot
MOVES=['N','S','E','W','NE','NW','SE','SW']
def passable(mem,x,y):
    t=mem[0x6000+(y>>3)*160+(x>>3)]; band=y>>8
    th=[0x38,0x06,0x0f][band]
    return t>=th
def scenario(seed):
    rnd=random.Random(seed)
    g=base(); rec=0xE4D0
    while True:
        x=rnd.randint(16,1260)&~1; y=rnd.randint(16,750)&~1
        if passable(g.mem,x,y): break
    place_player(g,0,x,y)
    g.mem[rec+3]=0x01; g.mem[rec+2]=0x20
    main=rnd.choice(MOVES)
    setpath(g,rec,[main if rnd.random()<0.7 else rnd.choice(MOVES) for _ in range(60)])
    last=0; junk=False
    for f in range(0,50*30,5):
        g.emap=set(); g.run(5)
        sp=g.reg[SP]; pc=g.reg[PC]
        if any(a in g.emap for a in (0xC2EC,0xC35B)): last=f
        if any(rec<=a<rec+0x61 for a in g.emap): junk=True
        if not (0x5E00<=sp<=0x5FF0) or pc<0x4000 or f-last>200:
            return dict(seed=seed,res='CRASH',x=x,y=y,cell=(y>>6)*20+(x>>6))
    return dict(seed=seed,res='survived' if junk else 'notrig',x=x,y=y,cell=(y>>6)*20+(x>>6))
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for s in range(a,b): print(json.dumps(scenario(s)),flush=True)
