import subprocess
N=0xD7; B=0xFF
PAL=[(0,0,0),(0,0,N),(N,0,0),(N,0,N),(0,N,0),(0,N,N),(N,N,0),(N,N,N),
     (0,0,0),(0,0,B),(B,0,0),(B,0,B),(0,B,0),(0,B,B),(B,B,0),(B,B,B)]
_T={}
def _tab(attr, flashphase):
    k=(attr,flashphase)
    t=_T.get(k)
    if t is None:
        ink=(attr&7)|((attr>>3)&8); paper=((attr>>3)&7)|((attr>>3)&8)
        if attr&0x80 and flashphase: ink,paper=paper,ink
        ci=bytes(PAL[ink]); cp=bytes(PAL[paper])
        t=[b''.join(ci if (v<<i)&0x80 else cp for i in range(8)) for v in range(256)]
        _T[k]=t
    return t
ROWADDR=[0x4000|((y&0xC0)<<5)|((y&7)<<8)|((y&0x38)<<2) for y in range(192)]
def render(mem, frame=0, border=0):
    fp=(frame//16)&1
    out=bytearray()
    bc=bytes(PAL[border&7])
    side=bc*16
    for _ in range(16): out+=bc*(256+32)
    for y in range(192):
        a=ROWADDR[y]; at=0x5800+(y>>3)*32
        out+=side
        for x in range(32):
            out+=_tab(mem[at+x],fp)[mem[a+x]]
        out+=side
    for _ in range(16): out+=bc*(256+32)
    return bytes(out)
class Recorder:
    def __init__(self, fn, fps=25, scale=3):
        self.p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','288x224','-r',str(fps),'-i','-',
            '-vf',f'scale={288*scale}:{224*scale}:flags=neighbor','-c:v','libx264','-pix_fmt','yuv420p','-crf','18',fn],stdin=subprocess.PIPE)
        self.n=0
    def frame(self, mem, frame=0):
        self.p.stdin.write(render(mem, frame)); self.n+=1
    def close(self):
        self.p.stdin.close(); self.p.wait()
