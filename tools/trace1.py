import sys; sys.path.insert(0,'.')
from fuzz import *
from skoolkit.simutils import SP
from skoolkit.traceutils import disassemble
g=Game('work/stonk.z80')
x,y=962,418; a=0xE450; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
g.run(800); g.tap('SP',5,20); g.run(150); g.tap('SP',5,20); g.run(200); g.tap('SP',5,20)
# now step to crash
hist=[]
for k in range(3000000):
    pc=g.reg[PC]; sp=g.reg[SP]
    hist.append((pc,sp))
    g.sim.trace(pc,-1,1,0,1,None,None,None,None,None)
    if g.reg[SP]>0x5FF0 and g.reg[SP]<0x6100:
        break
print('steps',k)
seen=[]
for pc,sp in hist[-400:]:
    seen.append('%04x/%04x %s'%(pc,sp,disassemble(g.mem,pc,'$','02X','04X')[0]))
print('\n'.join(seen[-140:]))
