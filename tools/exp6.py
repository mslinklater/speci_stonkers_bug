import sys; sys.path.insert(0,'.')
from exp import *
g=mkgame(932,420); rec=0xE4D0
r=watch(g,50*60*15,rec,every=25,verbose=False)
print(r, pos(g,rec), 'flags %02x'%g.mem[rec])
g.save('work/e6end.z80'); g.screenshot('work/e6end.png')
