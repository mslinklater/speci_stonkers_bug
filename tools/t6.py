import sys; sys.path.insert(0,'.')
from harness import *
g=Game('work/stonk.z80')
g.start_game()
g.save('work/ingame.z80')
for m in range(20):
    g.run(50*60)
    g.screenshot(f'work/t6_{m}.png')
    print(m, hex(g.reg[PC]), len(g.emap), flush=True)
g.savemap('work/map2.txt')
g.save('work/t6end.z80')
