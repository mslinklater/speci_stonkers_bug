import sys; sys.path.insert(0,'.')
from exp import *
from exp3 import setview, zoom

def mkgame2(units, enemies):
    g=Game('work/stonk.z80')
    for i,(x,y) in units.items():
        a=0xE450+4*i; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
    for i,(x,y) in enemies.items():
        a=0xE490+4*i; g.mem[a]=x&255; g.mem[a+1]=x>>8; g.mem[a+2]=y&255; g.mem[a+3]=y>>8
    g.start_game()
    return g

def epos(g,i):
    r=0xEAE0+0x22*i; m=g.mem
    return (m[r+0x13]|m[r+0x14]<<8, m[r+0x15]|m[r+0x16]<<8)

def watch2(g, frames, every=5, log=None):
    stuck=0; lastmain=0
    for f in range(0,frames,every):
        g.emap=set(); g.run(every)
        main = any(a in g.emap for a in (0xC2EC,0xC35B,0xC31C,0xC39E,0xC3D5))
        if main: lastmain=f
        if log: log(f)
        if f-lastmain > 250:
            return dict(frame=f, pc=g.reg[PC], sp=g.reg[SP], emap=sorted(g.emap))
    return None

if __name__=='__main__':
    g=mkgame2({0:(932,420)}, {0:(880,460)})
    def log(f):
        if f%250==0: print(f, 'P0',pos(g,0xE4D0),'%02x'%g.mem[0xE4D0],'E0',epos(g,0),'%02x'%g.mem[0xEAE0], flush=True)
    r=watch2(g, 50*240, log=log)
    if r: print('STUCK', r['frame'], hex(r['pc']), hex(r['sp']), ' '.join('%04x'%a for a in r['emap'][:80]))
    g.save('work/e7end.z80'); g.screenshot('work/e7end.png')
