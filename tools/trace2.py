import sys; sys.path.insert(0,'.')
from fuzz import *
from skoolkit.simutils import SP
g=Game('work/stonk.z80')
if len(sys.argv)>1:
    x,y=962,418; a=0xE450; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
g.run(800); g.tap('SP',5,20); g.run(150); g.tap('SP',5,20); g.run(200)
mx=0; mn=0xffff
for f in range(400):
    g.run(1); sp=g.reg[SP]; mx=max(mx,sp); mn=min(mn,sp)
    if f<40 or f%20==0: print(f,'pc %04x sp %04x'%(g.reg[PC],sp), 'flags0 %02x'%g.mem[0xE4D0], pos(g,0xE4D0))
print('max sp %04x min %04x'%(mx,mn))
