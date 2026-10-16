import sys, random, json; sys.path.insert(0,'.')
from exp7 import *
from exp3 import setview, zoom
from skoolkit.simutils import SP
MOVES=['N','S','E','W','NE','NW','SE','SW']
BASE=None
def base():
    g=Game('work/stonk.z80'); g.start_game(); return g
def place_player(g,i,x,y):
    r=0xE4D0+0x61*i; m=g.mem; m[r+0x52]=x&255; m[r+0x53]=x>>8; m[r+0x54]=y&255; m[r+0x55]=y>>8
def place_enemy(g,i,x,y):
    r=0xEAE0+0x22*i; m=g.mem; m[r+0x13]=x&255; m[r+0x14]=x>>8; m[r+0x15]=y&255; m[r+0x16]=y>>8
def scenario(seed, frames=50*150):
    rnd=random.Random(seed)
    g=base()
    units={}
    for i in rnd.sample(range(16), rnd.randint(1,6)):
        units[i]=(rnd.randint(940,1040)&~1, rnd.randint(330,420)&~1); place_player(g,i,*units[i])
    enemies={}
    for i in rnd.sample(range(16), rnd.randint(0,6)):
        enemies[i]=(rnd.randint(820,900)&~1, rnd.randint(430,520)&~1); place_enemy(g,i,*enemies[i])
    for i in range(16):
        if rnd.random()<0.7: g.mem[0xEAE0+0x22*i]&=0xFE
    zoomed=rnd.random()<0.5
    if zoomed:
        setview(g,13*64,6*64); g.run(20); zoom(g); g.run(20)
    for i in units:
        rec=0xE4D0+0x61*i
        main=rnd.choice(['SW','SW','W','S'])
        setpath(g,rec,[main if rnd.random()<0.7 else rnd.choice(MOVES) for _ in range(rnd.randint(20,120))])
    last=0
    for f in range(0,frames,10):
        g.emap=set(); g.run(10)
        sp=g.reg[SP]; pc=g.reg[PC]
        from monitor import suspicious
        sus=suspicious(g.emap)
        if sus: return dict(seed=seed, phase='junk', frame=f, sus=['%04x'%a for a in sus[:12]], **({'start':(x,y),'unit':i,'steps':steps,'cnt':cnt} if 'steps' in dir() else {'units':units,'enemies':enemies}))
        if any(a in g.emap for a in (0xC2EC,0xC35B,0xC3D5)): last=f
        bad = not (0x5E00<=sp<=0x5FF0) or pc<0x4000
        if bad or f-last>300:
            return dict(seed=seed, frame=f, pc=pc, sp=sp, zoomed=zoomed, units=units, enemies=enemies, emap=sorted(g.emap)[:40])
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
        if r: print(json.dumps(r), flush=True)
    print('done',a,b,flush=True)
