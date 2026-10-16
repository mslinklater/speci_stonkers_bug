import sys; sys.path.insert(0,'.')
from harness import *
g=Game('work/stonk.z80')
g.run(800)
g.screenshot('work/t2a.png')
g.tap('SP',5,100)
g.screenshot('work/t2b.png')
print(hex(g.reg[PC]), len(g.emap))
