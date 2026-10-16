import sys, collections; sys.path.insert(0,'.')
from harness import *
from skoolkit.simutils import SP
from skoolkit.traceutils import disassemble
g=Game(sys.argv[1])
rec=0xE4D0
def pos(r): m=g.mem; return (m[r+0x52]|m[r+0x53]<<8, m[r+0x54]|m[r+0x55]<<8)
print('unit0 before: flags %02x supply %02x cnt %d pos %s cell %02x'%(g.mem[rec],g.mem[rec+3],g.mem[rec+7],pos(rec),g.mem[rec+0x49]))
while g.reg[PC]!=0xE4D0:
    g.sim.trace(g.reg[PC],-1,1,0,1,None,None,None,None,None)
print('record bytes:', ' '.join('%02x'%b for b in g.mem[rec:rec+0x61]))
print('unit0 pos',pos(rec),'tile',(pos(rec)[0]>>3,pos(rec)[1]>>3),'cell %02x'%g.mem[rec+0x49])
for k in range(60):
    pc=g.reg[PC]; sp=g.reg[SP]
    print('%04x sp=%04x HL=%04x  %s'%(pc,sp,g.reg[6]*256+g.reg[7],disassemble(g.mem,pc,'$','02X','04X')[0]))
    g.sim.trace(pc,-1,1,0,1,None,None,None,None,None)
    if g.reg[PC]<0x4000 and k>3: 
        print('-> %04x sp=%04x'%(g.reg[PC],g.reg[SP])); break
