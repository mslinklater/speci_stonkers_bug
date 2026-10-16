import sys; sys.path.insert(0,'.')
from ui import *
from recorder import Recorder
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','videos')+'/'
g=Game('work/stonk.z80')
# put armoured division 0 on the east bank next to the bridge (demo placement)
g.rec=Recorder(OUT+'stonkers_gameplay.mp4')
g.run(800); g.tap('SP',5,100); g.run(150); g.tap('SP',5,20); g.run(200); g.tap('SP',5,20); g.run(150)
from fuzz2 import place_player
place_player(g,0,968,392)
# move overview cursor to the bridge
for i in range(200):
    vx,vy=view(g)
    keys=[]
    if vx<832: keys.append('M')
    if vy<384: keys.append('A')
    if not keys: break
    g.press(*keys); g.run(3)
g.press(); g.run(40)
print('view',view(g))
g.tap('1',3,10); g.run(80)
# select the unit and steer SW across the bridge
print('select',select_unit(g))
g.run(25)
g.tap('1',3,30)
for i in range(46):
    g.press('N','A'); g.run(4)
g.press(); g.run(25)
for k in range(5):
    if not g.mem[0xB564]: break
    g.tap('1',4,12)
print('cnt',g.mem[0xE4D7])
g.run(50*40)
print('end pos',pos(g,0xE4D0),'flags %02x'%g.mem[0xE4D0])
g.rec.close()
