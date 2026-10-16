import sys, random, json; sys.path.insert(0,'.')
import play
from play import *
SNAP=False
def battle(seed, minutes=30):
    rnd=random.Random(seed)
    tgt_port=[(1000,300),(968,380),(900,450),(860,500),(600,420),(400,300),(170,170)]
    tgt_hq  =[(1000,300),(968,380),(900,450),(860,500),(600,560),(300,650),(40,730)]
    play.WAY=None
    g=base()
    setview(g,1120,0); g.run(10); zoom(g); g.run(20)
    units=list(range(12)); routes={u:(tgt_port if u%2 else tgt_hq) for u in units}
    wp={u:0 for u in units}; t=0; jit=rnd.choice([0,0.05,0.15]); ended=None
    while t<minutes*60*50:
        for u in units:
            r=0xE4D0+0x61*u
            if g.mem[r]&0x83 or wp[u]>=len(routes[u]): continue
            x,y=pos(g,r); tx,ty=routes[u][wp[u]]
            if abs(tx-x)<12 and abs(ty-y)<12: wp[u]+=1; continue
            vx=max(0,min(0x460,(x-80)&~7)); vy=max(0,min(0x2A0,(y-48)&~7))
            setview(g,vx,vy); g.emap=set(); g.run(4)
            if not select_unit(g,r): continue
            g.tap('1',3,6); cx,cy=x,y; n=0
            while n<130:
                mv=step_toward(cx,cy,tx,ty,rnd,jit)
                if mv is None:
                    wp[u]+=1
                    if wp[u]>=len(routes[u]): break
                    tx,ty=routes[u][wp[u]]; continue
                g.emap=set(); g.press(*DIRKEYS[mv]); g.run(3); check(g,dict(seed=seed,phase='steer',unit=u,t=t))
                n+=1; cx+=2*(('E' in mv)-('W' in mv)); cy+=2*(('S' in mv)-('N' in mv))
                if not g.mem[0xB564]: break
            g.press(); g.run(3)
            if g.mem[0xB564]: g.tap('1',3,6)
        if SNAP: g.save('work/snap_%d.z80'%seed); open('work/snap_%d.t'%seed,'w').write(str(t))
        for k in range(20):
            g.emap=set(); g.run(10); t+=10
            check(g,dict(seed=seed,phase='run',t=t))
            if 0xC518 in g.emap:
                ended=t
                for j in range(60): g.emap=set(); g.run(10); check(g,dict(seed=seed,phase='ending',t=t))
                g.screenshot('work/battle_end_%d.png'%seed)
                return dict(seed=seed,res='ended',t=t,alive=sum(1 for u in units if not g.mem[0xE4D0+0x61*u]&1))
    return dict(seed=seed,res='timeout',wp=wp,alive=sum(1 for u in units if not g.mem[0xE4D0+0x61*u]&1),
                enemy_alive=sum(1 for i in range(12) if not g.mem[0xEAE0+0x22*i]&1))
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for s in range(a,b):
        try: print(json.dumps(battle(s)),flush=True)
        except Crash as e: print(json.dumps(dict(res='CRASH',**e.args[0])),flush=True)
