import sys; sys.path.insert(0,'.')
from harness import *
g=Game('work/stonk.z80')
g.run(800)
g.tap('SP',5,100)
g.run(150)
g.tap('SP',5,20)
shots(g,6,40,'t4')
