import sys; sys.path.insert(0,'.')
from fuzz import *
from skoolkit.simutils import SP
import ast
units=ast.literal_eval(sys.argv[1]); enemies=ast.literal_eval(sys.argv[2]) if len(sys.argv)>2 else {}
g=Game('work/stonk.z80')
for i,(x,y) in units.items():
    a=0xE450+4*i; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
for i,(x,y) in enemies.items():
    a=0xE490+4*i; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
seq=[('run',800),('tap','SP'),('run',150),('tap','SP'),('run',200),('tap','SP'),('run',300)]
f=0
for op,arg in seq:
    if op=='run':
        for k in range(arg):
            g.run(1); f+=1
            if not (0x5E00<=g.reg[SP]<=0x5FF0) and f>50:
                print('bad sp at frame',f,op,'pc %04x sp %04x'%(g.reg[PC],g.reg[SP])); sys.exit()
    else:
        g.tap(arg,5,20); f+=25
print('ok', f)
