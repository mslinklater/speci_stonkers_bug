import sys, random, json; sys.path.insert(0,'.')
from fuzz2 import *
from ui import DIRKEYS, view, select_unit
def scenario(seed):
    rnd=random.Random(seed)
    g=base()
    i=rnd.randrange(12) if rnd.random()<0.8 else rnd.randrange(12,16)
    rec=0xE4D0+0x61*i
    side=rnd.random()<0.7
    if side: x,y=rnd.randint(944,1040)&~1, rnd.randint(330,410)&~1
    else:    x,y=rnd.randint(840,900)&~1, rnd.randint(430,500)&~1
    place_player(g,i,x,y)
    others=[]
    for j in rnd.sample(range(16), rnd.randint(0,4)):
        if j!=i: place_player(g,j,rnd.randint(860,1040)&~1, rnd.randint(330,500)&~1); others.append(j)
    for k in range(16):
        if rnd.random()<0.5: g.mem[0xEAE0+0x22*k]&=0xFE
    setview(g,13*64,6*64); g.run(20); zoom(g); g.run(20)
    g.run(rnd.randint(0,30))
    if not select_unit(g,rec): return None
    g.run(rnd.randint(1,10))
    g.tap('1',3,rnd.randint(3,15))
    main = 'SW' if side else 'NE'
    alts = ['W','S'] if side else ['E','N']
    steps=[]
    for s in range(rnd.randint(10,140)):
        r=rnd.random()
        mv = main if r<0.55 else (rnd.choice(alts) if r<0.85 else rnd.choice(list(DIRKEYS)))
        steps.append(mv)
        g.emap=set(); g.press(*DIRKEYS[mv]); g.run(rnd.choice([2,3,4,6]))
        if not (0x5E00<=g.reg[SP]<=0x5FF0) or g.reg[PC]<0x4000:
            return dict(seed=seed, phase='steer', step=s, pc=g.reg[PC], sp=g.reg[SP], unit=i, start=(x,y), steps=steps)
    g.press(); g.run(rnd.randint(2,10)); cnt=g.mem[rec+7]
    g.tap('1',3,10)
    last=0
    for f in range(0,50*90,10):
        g.emap=set(); g.run(10)
        sp=g.reg[SP]; pc=g.reg[PC]
        from monitor import suspicious
        sus=suspicious(g.emap)
        if sus: return dict(seed=seed, phase='junk', frame=f, sus=['%04x'%a for a in sus[:12]], **({'start':(x,y),'unit':i,'steps':steps,'cnt':cnt} if 'steps' in dir() else {'units':units,'enemies':enemies}))
        if any(a in g.emap for a in (0xC2EC,0xC35B,0xC3D5)): last=f
        if not (0x5E00<=sp<=0x5FF0) or pc<0x4000 or f-last>300:
            return dict(seed=seed, phase='run', frame=f, pc=pc, sp=sp, unit=i, start=(x,y), cnt=cnt, steps=steps)
    return None
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for s in range(a,b):
        r=scenario(s)
        if r: print(json.dumps(r), flush=True)
    print('done',a,b,flush=True)
