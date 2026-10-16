def suspicious(emap):
    out=[a for a in emap if ((0xE450<=a<0xF1F0) and not (0xE450<=a<=0xE454) and not (0xE490<=a<=0xE4A0)) or (0x4000<=a<0x6000) or a==0x0038]
    return sorted(out)
