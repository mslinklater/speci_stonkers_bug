import sys; sys.path.insert(0,'.')
from ui import *
def run_order(start, moves, label, shots=False):
    g=mkgame2({0:start},{})
    setview(g,13*64,6*64); g.run(20); zoom(g); g.run(80)
    if not select_unit(g): return label, 'noselect'
    g.tap('1',3,10)
    for i,mv in enumerate(moves):
        g.emap=set(); g.press(*DIRKEYS[mv]); g.run(4)
        if not any(a in g.emap for a in (0xC3D5,0xC436)):
            return label, 'STUCK during steering at step %d pc %04x sp %04x'%(i,g.reg[PC],g.reg[SP]), g
    g.press(); g.run(5); cnt=g.mem[0xE4D7]
    g.tap('1',3,10)
    r=watch2(g, 50*60)
    if r: return label, 'STUCK after confirm frame %d pc %04x sp %04x cnt %d'%(r['frame'],r['pc'],r['sp'],cnt), g
    return label, 'ok cnt %d end %s flags %02x'%(cnt, pos(g,0xE4D0), g.mem[0xE4D0]), g
tests=[
 ('SW', (976,384), ['SW']*40),
 ('W', (984,400), ['W']*40),
 ('S', (944,360), ['S']*40),
 ('SWW', (984,392), ['SW','W']*20),
 ('SWS', (968,376), ['SW','S']*20),
]
if __name__=='__main__':
    for label,start,moves in tests:
        res=run_order(start,moves,label)
        print(res[0],start,res[1],flush=True)
