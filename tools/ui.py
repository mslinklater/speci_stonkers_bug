import sys; sys.path.insert(0,'.')
from exp7 import *
DIRKEYS={'E':['M'],'W':['N'],'N':['Q'],'S':['A'],'NE':['M','Q'],'NW':['N','Q'],'SE':['M','A'],'SW':['N','A']}
def view(g): m=g.mem; return (m[0xBDF4]|m[0xBDF5]<<8, m[0xBDF6]|m[0xBDF7]<<8)
def select_unit(g, rec=0xE4D0):
    x,y=pos(g,rec); vx,vy=view(g)
    bx=x-vx+0x20; cy=y-vy+0x20
    for dx in range(-14,4,2):
        for dy in range(-14,4,2):
            g.mem[0xBBAE]=max(0,bx-0x27+dx+7)&0xFE; g.mem[0xBBAF]=max(0,cy-0x27+dy+7)&0xFE
            g.run(3)
            if g.mem[rec]&0x10:
                return True
    return False
def order(g, moves, rec=0xE4D0, frames_per=2):
    g.tap('1',3,10)   # fire: select
    for mv in moves:
        g.press(*DIRKEYS[mv]); g.run(frames_per)
    g.press(); g.run(5)
    g.tap('1',3,10)   # fire: confirm
