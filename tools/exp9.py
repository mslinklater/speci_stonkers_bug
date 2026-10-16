import sys; sys.path.insert(0,'.')
from ui import *
g=mkgame2({0:(976,392)},{})
setview(g,13*64,6*64); g.run(20); zoom(g); g.run(80)
print('view',view(g),'unitpos',pos(g,0xE4D0))
ok=select_unit(g); print('selected',ok, 'cursor',g.mem[0xBBAE],g.mem[0xBBAF], 'flags %02x'%g.mem[0xE4D0])
g.screenshot('work/e9a.png')
g.tap('1',3,10)
print('after fire: flags %02x cnt %d BDFF %d B564 %d'%(g.mem[0xE4D0],g.mem[0xE4D7],g.mem[0xBDFF],g.mem[0xB564]))
for i in range(20):
    g.press('N'); g.run(2)
print('after W: flags %02x cnt %d'%(g.mem[0xE4D0],g.mem[0xE4D7]), 'cursor',g.mem[0xBBAE],g.mem[0xBBAF])
g.press(); g.run(5)
g.screenshot('work/e9b.png')
