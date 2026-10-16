import sys, collections; sys.path.insert(0,'.')
from fuzz import *
from skoolkit.simutils import SP, T
from skoolkit.traceutils import disassemble
known=set(int(l.strip()[1:],16) for l in open('work/mapall.txt'))
# add code seen in UI/zoom runs
g0=mkgame2({0:(976,392)},{}); setview(g0,13*64,6*64); g0.run(20); zoom(g0); g0.run(80); known|=g0.emap
g=Game('work/stonk.z80')
x,y=962,418; a=0xE450; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
g.run(800); g.tap('SP',5,20); g.run(150); g.tap('SP',5,20); g.run(200)
g.press('SP')
hist=collections.deque(maxlen=400)
t_release=g.reg[T]+5*FRAME; released=False
for k in range(20000000):
    if not released and g.reg[T]>=t_release: g.press(); released=True
    pc=g.reg[PC]
    if pc>=0x4000 and pc not in known: break
    hist.append((pc,g.reg[SP]))
    g.sim.trace(pc,-1,1,0,1,None,None,None,None,None)
print('left known code at pc %04x after %d steps'%(pc,k))
for p,sp in list(hist)[-120:]:
    print('%04x sp=%04x  %s'%(p,sp,disassemble(g.mem,p,'$','02X','04X')[0]))
