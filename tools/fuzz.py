import sys, random, json; sys.path.insert(0,'.')
from exp7 import *
from exp3 import setview, zoom
MOVES=['N','S','E','W','NE','NW','SE','SW']
def scenario(seed):
    rnd=random.Random(seed)
    units={}
    for i in rnd.sample(range(16), rnd.randint(1,6)):
        units[i]=(rnd.randint(940,1040)&~1, rnd.randint(330,420)&~1)
    enemies={}
    for i in rnd.sample(range(16), rnd.randint(0,6)):
        enemies[i]=(rnd.randint(820,900)&~1, rnd.randint(430,520)&~1)
    g=mkgame2(units, enemies)
    for i in range(16):
        if rnd.random()<0.7: g.mem[0xEAE0+0x22*i]&=0xFE
    zoomed=rnd.random()<0.5
    if zoomed:
        setview(g,13*64,6*64); g.run(20); zoom(g); g.run(60)
    # give orders: mostly SW with jitter
    for i in units:
        rec=0xE4D0+0x61*i
        main=rnd.choice(['SW','SW','W','S'])
        path=[main if rnd.random()<0.7 else rnd.choice(MOVES) for _ in range(rnd.randint(20,120))]
        setpath(g,rec,path)
    stuck=0; last=0
    for f in range(0,50*150,10):
        g.emap=set(); g.run(10)
        if any(a in g.emap for a in (0xC2EC,0xC35B,0xC3D5)): last=f
        elif f-last>300:
            return dict(seed=seed, frame=f, pc=g.reg[PC], sp=g.reg[SP], zoomed=zoomed, units=units, enemies=enemies,
                        emap=sorted(g.emap)[:60])
        # occasionally re-order units that stopped
        if f%500==0:
            for i in units:
                rec=0xE4D0+0x61*i
                if not g.mem[rec]&0x81 and rnd.random()<0.5:
                    main=rnd.choice(MOVES)
                    setpath(g,rec,[main if rnd.random()<0.6 else rnd.choice(MOVES) for _ in range(rnd.randint(10,80))])
    return None
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for s in range(a,b):
        r=scenario(s)
        if r:
            print(json.dumps(r), flush=True)
    print('done',a,b,flush=True)
