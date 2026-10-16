import sys; sys.path.insert(0,'.')
from harness import *
g=Game('work/stonk.z80')
g.run(800)
g.tap('SP',5,100)
for i in range(6):
    g.run(25); g.screenshot(f'work/t3_{i}.png')
