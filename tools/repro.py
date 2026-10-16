import sys, random; sys.path.insert(0,'.')
from fuzz import *
from skoolkit.simutils import SP
def build(seed):
    rnd=random.Random(seed)
    units={}
    for i in rnd.sample(range(16), rnd.randint(1,6)):
        units[i]=(rnd.randint(940,1040)&~1, rnd.randint(330,420)&~1)
    enemies={}
    for i in rnd.sample(range(16), rnd.randint(0,6)):
        enemies[i]=(rnd.randint(820,900)&~1, rnd.randint(430,520)&~1)
    g=mkgame2(units, enemies)
    for i in range(16):
        if rnd.random()<0.7: g.mem[0xEAE0+0x22*i]&=0xFE
    zoomed=rnd.random()<0.5
    if zoomed:
        setview(g,13*64,6*64); g.run(20); zoom(g); g.run(60)
    paths={}
    for i in units:
        rec=0xE4D0+0x61*i
        main=rnd.choice(['SW','SW','W','S'])
        path=[main if rnd.random()<0.7 else rnd.choice(MOVES) for _ in range(rnd.randint(20,120))]
        paths[i]=path
    return g, units, enemies, zoomed, paths
if __name__=='__main__':
    seed=int(sys.argv[1])
    g,units,enemies,zoomed,paths=build(seed)
    print('units',units,'enemies',enemies,'zoomed',zoomed)
    for i in units:
        rec=0xE4D0+0x61*i
        print(' unit',i,'flags %02x type %02x pos %s'%(g.mem[rec],g.mem[rec+1],pos(g,rec)), 'path',len(paths[i]), ''.join(m[0] if len(m)==1 else m.lower() for m in paths[i][:40]))
    for i in units: setpath(g,0xE4D0+0x61*i,paths[i])
    for f in range(400):
        g.run(1)
        sp=g.reg[SP]; pc=g.reg[PC]
        if not (0x5F00<=sp<=0x5FF0) or pc<0x4000:
            print('CRASH at frame',f,'pc %04x sp %04x'%(pc,sp)); break
        if f%10==0:
            print(f, ' '.join('u%d:%s:%02x:%d'%(i,pos(g,0xE4D0+0x61*i),g.mem[0xE4D0+0x61*i],g.mem[0xE4D0+0x61*i+7]) for i in units))
