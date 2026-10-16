import sys; sys.path.insert(0,'.')
from exp7 import *
g=mkgame2({0:(932,420)}, {0:(880,460)})
g.mem[0xEAE0]&=0xFE
def log(f):
    if f%50==0: print(f, 'P0',pos(g,0xE4D0),'%02x'%g.mem[0xE4D0],'E0',epos(g,0),'%02x'%g.mem[0xEAE0], 'dir',g.mem[0xEAE7],'tgt %02x'%g.mem[0xEAE8],'cell %02x'%g.mem[0xEAEA], flush=True)
r=watch2(g, 50*120, log=log)
if r: print('STUCK', r['frame'], hex(r['pc']), hex(r['sp']), ' '.join('%04x'%a for a in r['emap'][:120]))
g.save('work/e8end.z80'); g.screenshot('work/e8end.png')
