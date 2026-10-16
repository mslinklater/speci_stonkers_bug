import sys, random, json, pickle; sys.path.insert(0,'.')
import play
from play import *
from harness import Game
from skoolkit.simutils import SP
class LGame(Game):
    def __init__(self,*a,**k):
        super().__init__(*a,**k); self.actions=[]; self.ctx=''; self.checking=False; self.snapidx=0; self.seed=0
    def press(self,*keys):
        self.actions.append(('press',keys)); super().press(*keys)
    def run(self,frames=1,stop=-1,emap=True):
        self.actions.append(('run',frames))
        r=super().run(frames,stop,emap)
        if self.checking:
            sp=self.reg[SP]; pc=self.reg[PC]
            if pc==0x0038 or not (0x5E00<=sp<=0x5FF2) or pc<0x4000 or (0xE455<=pc<0xF1F0 and not 0xE490<=pc<=0xE4A0):
                raise Crash(dict(seed=self.seed,ctx=self.ctx,pc=pc,sp=sp,snapidx=self.snapidx,nact=len(self.actions)))
        return r
    def checkpoint(self,name):
        self.save(name); self.snapidx=len(self.actions)
def battle(seed, minutes=30, snapfile=None):
    rnd=random.Random(seed)
    tgt_port=[(1000,300),(968,380),(900,450),(860,500),(600,420),(400,300),(170,170)]
    tgt_hq  =[(1000,300),(968,380),(900,450),(860,500),(600,560),(300,650),(40,730)]
    g=LGame('work/stonk.z80'); g.seed=seed; g.start_game(); g.checking=True
    setview(g,1120,0); g.run(10); zoom(g); g.run(20)
    units=list(range(12)); routes={u:(tgt_port if u%2 else tgt_hq) for u in units}
    wp={u:0 for u in units}; t=0; jit=rnd.choice([0,0.05,0.15])
    while t<minutes*60*50:
        for u in units:
            r=0xE4D0+0x61*u
            if g.mem[r]&0x83 or wp[u]>=len(routes[u]): continue
            x,y=pos(g,r); tx,ty=routes[u][wp[u]]
            if abs(tx-x)<12 and abs(ty-y)<12: wp[u]+=1; continue
            if snapfile: g.checkpoint(snapfile)
            g.ctx='order unit %d at %s -> %s t=%d'%(u,(x,y),(tx,ty),t)
            vx=max(0,min(0x460,(x-80)&~7)); vy=max(0,min(0x2A0,(y-48)&~7))
            setview(g,vx,vy); g.run(4)
            if not select_unit(g,r): continue
            g.tap('1',3,6); cx,cy=x,y; n=0
            while n<130:
                mv=step_toward(cx,cy,tx,ty,rnd,jit)
                if mv is None:
                    wp[u]+=1
                    if wp[u]>=len(routes[u]): break
                    tx,ty=routes[u][wp[u]]; continue
                g.press(*DIRKEYS[mv]); g.run(3)
                n+=1; cx+=2*(('E' in mv)-('W' in mv)); cy+=2*(('S' in mv)-('N' in mv))
                if not g.mem[0xB564]: break
            g.press(); g.run(3)
            if g.mem[0xB564]: g.tap('1',3,6)
        if snapfile: g.checkpoint(snapfile)
        g.ctx='run t=%d'%t
        for k in range(20):
            g.emap=set(); g.run(10); t+=10
            if 0xC518 in g.emap:
                return dict(seed=seed,res='ended',t=t), g
    return dict(seed=seed,res='timeout'), g
if __name__=='__main__':
    seed=int(sys.argv[1])
    try: print(battle(seed, snapfile='work/cp_%d.z80'%seed)[0])
    except Crash as e:
        info=e.args[0]; print('CRASH',info)
        g=sys.modules['__main__']
