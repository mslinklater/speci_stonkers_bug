import sys, random, json; sys.path.insert(0,'.')
from fuzz2 import *
PATTERNS={'SW only':['SW'],'W+SW':['W','SW'],'S+SW':['S','SW'],'W,W,SW':['W','W','SW'],'S,S,SW':['S','S','SW'],'W only':['W'],'S only':['S']}
def scenario(name, seed):
    rnd=random.Random(seed)
    g=base(); rec=0xE4D0
    x=rnd.randint(960,1000)&~1; y=rnd.randint(340,390)&~1
    place_player(g,0,x,y)
    g.mem[rec+3]=0x01; g.mem[rec+2]=rnd.choice([0x20,0x40,0x60,0x80,0xA0,0xC0,0xE0,0x00])
    pat=PATTERNS[name]; off=rnd.randrange(len(pat))
    setpath(g,rec,[pat[(k+off)%len(pat)] for k in range(rnd.randint(40,120))])
    last=0; junk=False
    for f in range(0,50*30,5):
        g.emap=set(); g.run(5)
        sp=g.reg[SP]; pc=g.reg[PC]
        if any(a in g.emap for a in (0xC2EC,0xC35B)): last=f
        if any(rec<=a<rec+0x61 for a in g.emap): junk=True
        if not (0x5E00<=sp<=0x5FF0) or pc<0x4000 or f-last>200:
            return 'CRASH'
    return 'survived' if junk else 'notrig'
if __name__=='__main__':
    name=sys.argv[1]; import collections; c=collections.Counter()
    for s in range(60): c[scenario(name,s)]+=1
    print(json.dumps({'pattern':name, **c}),flush=True)
