import sys; sys.path.insert(0,'.')
from harness import *
from skoolkit.simutils import SP

NIB={'N':3,'S':7,'E':0xD,'W':0xC,'NE':1,'NW':0,'SE':5,'SW':4}
def setpath(g, rec, moves):
    m=g.mem; n=len(moves); assert n<=128
    for i in range(64): m[rec+8+i]=0
    for i in range(n):
        nib=NIB[moves[n-1-i]]
        a=rec+8+i//2
        if i%2==0: m[a]=(m[a]&0xF0)|nib
        else: m[a]=(m[a]&0x0F)|(nib<<4)
    m[rec+7]=n
    m[rec]|=0x80

def mkgame(x,y,unit=0):
    g=Game('work/stonk.z80')
    a=0xE450+4*unit
    g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
    g.start_game()
    return g

def pos(g,rec):
    m=g.mem; return (m[rec+0x52]|m[rec+0x53]<<8, m[rec+0x54]|m[rec+0x55]<<8)

def watch(g, frames, rec, every=10, verbose=True):
    """run, return (crashed, info)"""
    for f in range(0,frames,every):
        g.emap=set()
        g.run(every)
        sp=g.reg[SP]; pc=g.reg[PC]
        mainloop = any(a in g.emap for a in (0xC2EC,0xC35B,0xC31C,0xC39E))
        if verbose and f%100==0:
            print(f, 'pos',pos(g,rec),'flags %02x cnt %d'%(g.mem[rec],g.mem[rec+7]),'sp %04x pc %04x'%(sp,pc), flush=True)
        if not mainloop or sp<0x5E00 or sp>0x5FF0:
            return True, dict(frame=f, sp=sp, pc=pc, pos=pos(g,rec))
    return False, None

if __name__=='__main__':
    g=mkgame(976,392)
    rec=0xE4D0
    print('start', pos(g,rec), 'flags %02x speed %d'%(g.mem[rec],g.mem[rec+6]))
    setpath(g,rec,['W']*10+['SW','W']*30)
    print(watch(g,3000,rec))
    g.screenshot('work/exp1.png')
