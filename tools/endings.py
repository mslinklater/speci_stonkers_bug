import sys, json; sys.path.insert(0,'.')
from fuzz2 import *
from monitor import suspicious
from recorder import Recorder
from skoolkit.simutils import SP
def setup(kind, g):
    m=g.mem
    m[0xBBF0]=0   # all enemy units released
    for i in range(16): m[0xEAE0+0x22*i]&=0xFE
    if kind=='all_enemy_dead':
        for i in range(12): m[0xEAE0+0x22*i]|=0x01
    elif kind=='occupy_enemy':
        # player units 0,1 standing in enemy port (2A) and enemy HQ (DC)
        for u,cell in ((0,0x2A),(1,0xDC)):
            r=0xE4D0+0x61*u; m[r+0x49]=cell
    elif kind=='enemy_occupies':
        for u,cell in ((0,0x13),(1,0x4B)):
            r=0xEAE0+0x22*u; m[r+0x0A]=cell
        for u in range(12):
            r=0xE4D0+0x61*u
            if m[r+0x49] in (0x13,0x4B): m[r+0x49]=0x50
    elif kind=='all_player_dead':
        for i in range(12): m[0xE4D0+0x61*i]|=0x01
def run(kind, video=None):
    g=base()
    if video: g.rec=Recorder(video)
    g.run(100)
    setup(kind,g)
    events=[]; seen_end=False
    for f in range(0,50*40,5):
        g.emap=set(); g.run(5)
        sus=suspicious(g.emap); sp=g.reg[SP]; pc=g.reg[PC]
        if 0xC518 in g.emap and not seen_end: events.append(('end-sequence',f)); seen_end=True
        if 0xC1AD in g.emap: events.append(('restart',f))
        if sus or not (0x5E00<=sp<=0x5FF2) or pc<0x4000:
            events.append(('CRASH',f,'pc %04x sp %04x'%(pc,sp),' '.join('%04x'%a for a in sus[:8])))
            break
        if events and events[-1][0]=='restart':
            g.run(50); g.tap('SP',5,50)   # press a key for next battle
    if video:
        g.run(100); g.rec.close()
    return kind, events
if __name__=='__main__':
    print(run(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None))
