import sys, pickle, collections; sys.path.insert(0,'.')
from harness import *
from skoolkit.simutils import SP
from skoolkit.traceutils import disassemble
seed=int(sys.argv[1])
acts=pickle.load(open('work/cp_%d.acts'%seed,'rb'))
print(acts)
g=Game('work/cp_%d.z80'%seed)
def bad(pc,sp): return pc==0x0038 or not (0x5E00<=sp<=0x5FF2) or pc<0x4000 or (0xE455<=pc<0xF1F0 and not 0xE490<=pc<=0xE4A0)
# replay all but the failing run action normally, check after each
for i,(op,arg) in enumerate(acts):
    if op=='press': g.press(*arg); continue
    st=(g.reg[PC],g.reg[SP])
    g.save('work/pre_%d.z80'%i)
    g.run(arg)
    if bad(g.reg[PC],g.reg[SP]):
        print('crash during action',i,op,arg,'pc %04x sp %04x'%(g.reg[PC],g.reg[SP])); break
    print('action',i,op,arg,'ok', 'B564=%02x BBAE=%d BBAF=%d cnt=%d'%(g.mem[0xB564],g.mem[0xBBAE],g.mem[0xBBAF],g.mem[0xE4D0+0x61*9+7]))
