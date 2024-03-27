def get_level(xp,xp_type):
    i,lvl = 0,1
    if xp_type==1:
        while i<xp:
            lvl+=1
            i=(lvl**3)*0.8
        return lvl-1
    elif xp_type==2:
        while i<xp:
            lvl+=1
            i=lvl**3
        return lvl-1
    elif xp_type==3:
        while i<xp:
            lvl+=1
            i=1.2*(lvl**3)-15*(lvl**2)+100*lvl-140
        return lvl-1
    else:
        while i<xp:
            lvl+=1
            i=1.25*(lvl**3)
        return lvl-1
    
print(get_level(352144,1))