import sys; sys.path.insert(0,'.')
from exp3 import *
g=mkgame(976,368); rec=0xE4D0
setview(g,13*64,6*64)
g.run(20)
zoom(g)
g.run(100)
g.screenshot('work/e4a.png')
print(pos(g,rec), [hex(g.mem[a]) for a in range(0xBDF4,0xBDFC)])
