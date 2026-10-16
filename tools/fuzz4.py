import sys, random, json; sys.path.insert(0,'.')
from fuzz2 import *
from exp import NIB
MOVES=['N','S','E','W','NE','NW','SE','SW']
def scenario(seed):
    rnd=random.Random(seed)
    g=base(); rec=0xE4D0
    x=rnd.randint(930,1010)&~1; y=rnd.randint(340,420)&~1
    place_player(g,0,x,y)
    g.mem[rec+3]=0x01; g.mem[rec+2]=rnd.choice([0x20,0x40,0x60,0x80])
    main=rnd.choice(['SW','SW','W','S'])
    path=[main if rnd.random()<0.7 else rnd.choice(MOVES) for _ in range(rnd.randint(30,120))]
    setpath(g,rec,path)
    allmap=set(); last=0
    for f in range(0,50*40,5):
        g.emap=set(); g.run(5); allmap|=g.emap
        sp=g.reg[SP]; pc=g.reg[PC]
        if any(a in g.emap for a in (0xC2EC,0xC35B)): last=f
        if not (0x5E00<=sp<=0x5FF0) or pc<0x4000 or f-last>200:
            return dict(seed=seed,res='CRASH',f=f,pc=pc,sp=sp,start=(x,y),endpos=pos(g,rec))
    ran = any(rec<=a<rec+0x61 for a in allmap)
    return dict(seed=seed,res='survived' if ran else 'notriggered',start=(x,y),endpos=pos(g,rec))
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for s in range(a,b): print(json.dumps(scenario(s)),flush=True)
