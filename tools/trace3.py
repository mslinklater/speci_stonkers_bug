import sys, collections; sys.path.insert(0,'.')
from fuzz import *
from skoolkit.simutils import SP, T
from skoolkit.traceutils import disassemble
g=Game('work/stonk.z80')
x,y=962,418; a=0xE450; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
g.run(800); g.tap('SP',5,20); g.run(150); g.tap('SP',5,20); g.run(200)
g.press('SP')
hist=collections.deque(maxlen=3000)
t_release=g.reg[T]+5*FRAME
released=False
for k in range(20000000):
    if not released and g.reg[T]>=t_release: g.press(); released=True
    pc=g.reg[PC]; sp=g.reg[SP]
    hist.append((pc,sp,g.reg[0],g.reg[2]*256+g.reg[3] if False else 0))
    g.sim.trace(pc,-1,1,0,1,None,None,None,None,None)
    if g.reg[SP]>0x5FF0 and g.reg[SP]<0x6100:
        break
print('steps',k)
for pc,sp,a,_ in list(hist)[-160:]:
    print('%04x sp=%04x  %s'%(pc,sp,disassemble(g.mem,pc,'$','02X','04X')[0]))
