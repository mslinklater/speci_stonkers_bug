import sys, random, json; sys.path.insert(0,'.')
from fuzz2 import *
from ui import DIRKEYS, view, select_unit
from monitor import suspicious
from skoolkit.simutils import SP
WAY=[(1000,300),(968,380),(900,450),(860,500),(700,560)]
def step_toward(x,y,tx,ty,rnd,jit):
    dx = 'E' if tx>x+2 else ('W' if tx<x-2 else '')
    dy = 'S' if ty>y+2 else ('N' if ty<y-2 else '')
    if rnd.random()<jit: return rnd.choice(list(DIRKEYS))
    if dx and dy and rnd.random()<0.3: return rnd.choice([dx,dy])
    return (dy+dx) if (dx or dy) else None
class Crash(Exception): pass
def check(g,info):
    sus=suspicious(g.emap); sp=g.reg[SP]; pc=g.reg[PC]
    if sus or not (0x5E00<=sp<=0x5FF0) or pc<0x4000:
        raise Crash(dict(info, sus=['%04x'%a for a in sus[:10]], pc=pc, sp=sp))
def play(seed, units=(0,1,2,3), minutes=12, rec=None):
    rnd=random.Random(seed); jit=rnd.choice([0,0.05,0.15,0.3])
    g=base(); g.rec=rec
    # zoom into HQ area
    setview(g, 1120, 0); g.run(10); zoom(g); g.run(20)
    t=0; wp={u:0 for u in units}; log=[]
    while t < minutes*60*50:
        for u in units:
            r=0xE4D0+0x61*u
            if g.mem[r]&0x83: continue   # dead/moving/in combat
            if wp[u]>=len(WAY): continue
            x,y=pos(g,r)
            tx,ty=WAY[wp[u]]
            if abs(tx-x)<12 and abs(ty-y)<12:
                wp[u]+=1; continue
            vx=max(0,min(0x460,(x-80)&~7)); vy=max(0,min(0x2A0,(y-48)&~7))
            setview(g,vx,vy); g.emap=set(); g.run(4)
            if not select_unit(g,r): continue
            g.tap('1',3,6)
            cx,cy=x,y; n=0
            while n<130:
                mv=step_toward(cx,cy,tx,ty,rnd,jit)
                if mv is None:
                    wp[u]+=1
                    if wp[u]>=len(WAY): break
                    tx,ty=WAY[wp[u]]; continue
                g.emap=set(); g.press(*DIRKEYS[mv]); g.run(3); check(g,dict(seed=seed,phase='steer',unit=u))
                n+=1
                cx+= 2*(('E' in mv)-('W' in mv)); cy+=2*(('S' in mv)-('N' in mv))
                if not (g.mem[0xB564]): break   # order loop exited (auto-finish at 128)
            g.press(); g.run(3)
            if g.mem[0xB564]: g.tap('1',3,6)
            log.append((t,u,(x,y),wp[u],n))
        for k in range(20):
            g.emap=set(); g.run(10); t+=10
            check(g,dict(seed=seed,phase='run',t=t))
    return dict(seed=seed,res='ok',jit=jit,pos={u:pos(g,0xE4D0+0x61*u) for u in units},flags={u:'%02x'%g.mem[0xE4D0+0x61*u] for u in units},wp=wp,orders=len(log))
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for s in range(a,b):
        try: print(json.dumps(play(s)),flush=True)
        except Crash as e: print(json.dumps(dict(res='CRASH',**e.args[0])),flush=True)
