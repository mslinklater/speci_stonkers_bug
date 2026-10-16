import sys, json; sys.path.insert(0,'.')
from fuzz2 import *
from ui import DIRKEYS, view, select_unit
from monitor import suspicious
from skoolkit.simutils import SP
def overview_to_bridge(g):
    for i in range(200):
        vx,vy=view(g); keys=[]
        if vx<832: keys.append('M')
        if vy<384: keys.append('A')
        if not keys: break
        g.press(*keys); g.run(3)
    g.press(); g.run(30)
def demo(route, supply=0x02, counter=0x20, rec=None, after=50*25):
    g=base(); g.rec=rec
    place_player(g,0,968,392)
    g.run(60)
    overview_to_bridge(g)
    g.tap('1',3,10); g.run(60)
    r=0xE4D0
    assert select_unit(g,r)
    g.run(40)
    g.mem[r+3]=supply; g.mem[r+2]=counter
    g.tap('1',3,30)
    for mv in route:
        g.press(*DIRKEYS[mv]); g.run(4)
    g.press(); g.run(25)
    if g.mem[0xB564]: g.tap('1',3,10)
    events=[]; last=0
    for f in range(0,after,5):
        g.emap=set(); g.run(5)
        sp=g.reg[SP]; pc=g.reg[PC]
        if any(a in g.emap for a in (0xC35B,0xC2EC)): last=f
        if any(0xE4D0<=a<0xE531 for a in g.emap) and not events: events.append(('record-executed',f,pos(g,r)))
        if not (0x5E00<=sp<=0x5FF2) or pc<0x4000 or f-last>150:
            events.append(('CRASH',f,'pc %04x sp %04x'%(pc,sp),pos(g,r))); break
        if g.mem[r]&1 and ('dead' not in [e[0] for e in events]): events.append(('dead',f,pos(g,r)))
    return events, g
if __name__=='__main__':
    routes={
     'SWx40':['SW']*40,
     'SW30W30':['SW']*30+['W']*30,
     'SW,W x30':['SW','W']*30,
     'SW,SW,W x20':['SW','SW','W']*20,
     'SW30S30':['SW']*30+['S']*30,
     'SW,S x30':['SW','S']*30,
    }
    for name,rt in routes.items():
        ev,g=demo(rt); print(name, ev, flush=True)
