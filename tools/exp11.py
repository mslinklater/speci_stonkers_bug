import sys; sys.path.insert(0,'.')
from fuzz2 import *
from skoolkit.traceutils import disassemble
def test(path, supply=0x01, label=''):
    g=base(); rec=0xE4D0
    place_player(g,0,976,384)
    g.mem[rec+3]=supply
    setpath(g,rec,path)
    for f in range(0,50*60,5):
        g.emap=set(); g.run(5)
        sp=g.reg[SP]; pc=g.reg[PC]
        main=any(a in g.emap for a in (0xC2EC,0xC35B,0xC3D5))
        if not (0x5E00<=sp<=0x5FF0) or pc<0x4000 or (rec<=pc<rec+0x61):
            return label,'CRASH frame %d pc %04x sp %04x'%(f,pc,sp), g
        if not main and f>200:
            return label,'STUCK frame %d pc %04x sp %04x'%(f,pc,sp), g
    return label,'ok flags %02x supply %02x'%(g.mem[rec],g.mem[rec+3]), g
for label,path in [('SW',['SW']*100),('W',['W']*100),('S',['S']*100),('SWW',['SW','W']*50),('E',['E']*100)]:
    r=test(path,label=label); print(r[0],r[1],flush=True)
