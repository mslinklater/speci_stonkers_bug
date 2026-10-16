import sys,struct
d=open(sys.argv[1],'rb').read()
i=0;n=0;blocks=[]
while i<len(d):
    L=struct.unpack('<H',d[i:i+2])[0]
    blocks.append(d[i+2:i+2+L]); i+=2+L
for k,b in enumerate(blocks):
    if b[0]==0xff:
        open(f'work/blk{k}.bin','wb').write(b[1:-1])
