import sys; sys.path.insert(0,'.')
from exp import *
def setview(g, vx, vy):
    m=g.mem
    m[0xBDF4]=vx&255; m[0xBDF5]=vx>>8; m[0xBDF6]=vy&255; m[0xBDF7]=vy>>8
    p=0x6000+(vy>>3)*160+(vx>>3); m[0xBDFD]=p&255; m[0xBDFE]=p>>8
def zoom(g):
    g.tap('1',3,30)
if __name__=='__main__':
    g=mkgame(976,368); rec=0xE4D0
    setview(g,13*64,6*64)
    g.run(20)
    g.screenshot('work/e3a.png')
    zoom(g)
    g.screenshot('work/e3b.png')
    print('BDFC',g.mem[0xBDFC], [hex(g.mem[a]) for a in range(0xBDF4,0xBDFC)])
