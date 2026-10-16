import sys, collections; sys.path.insert(0,'.')
from harness import *
from skoolkit.simutils import SP
from skoolkit.traceutils import disassemble
g=Game(sys.argv[1])
hist=collections.deque(maxlen=int(sys.argv[2]) if len(sys.argv)>2 else 300)
def bad(pc,sp):
    return pc==0x0038 or (0xE455<=pc<0xF1F0 and not 0xE490<=pc<=0xE4A0) or not (0x5E00<=sp<=0x5FF2) or (0x4000<=pc<0x6000)
for k in range(5000000):
    pc=g.reg[PC]; sp=g.reg[SP]
    if bad(pc,sp): break
    hist.append((pc,sp,g.reg[0],g.reg[1]))
    g.sim.trace(pc,-1,1,0,1,None,None,None,None,None)
print('stopped after',k,'pc %04x sp %04x'%(g.reg[PC],g.reg[SP]))
for p,sp,a,f in hist:
    print('%04x sp=%04x a=%02x  %s'%(p,sp,a,disassemble(g.mem,p,'$','02X','04X')[0]))
