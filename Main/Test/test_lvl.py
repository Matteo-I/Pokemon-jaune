from random import randint



def get_level(xp,xp_type):
    '''
    return le niveau du pokemon en fonction de son xp actuelle et de sa courbe d'xp
        '''
    i,lvl = 0,1
    if xp_type==1:
        #Courbe rapide
        while i<xp:
            lvl+=1
            i=(lvl**3)*0.8
        return lvl-1
    elif xp_type==2:
        #Courbe moyenne
        while i<xp:
            lvl+=1
            i=lvl**3
        return lvl-1
    elif xp_type==3:
        #Courbe parabolique
        while i<xp:
            lvl+=1
            i=1.2*(lvl**3)-15*(lvl**2)+100*lvl-140
        return lvl-1
    else:
        #Courbe lente
        while i<xp:
            lvl+=1
            i=1.25*(lvl**3)
        return lvl-1
        
def get_xp(lvl,xp_type):
    '''
    return l'xp du pokemon en fonction d'un niveau donné et de sa courbe d'xp
    Cette methode sert uniquement a la generation d'un pokemon avec un niveau defini
    '''
    if xp_type==1:
        #Courbe rapide
        result= (lvl**3)*0.8
    elif xp_type==2:
        #Courbe moyenne
        result= lvl**3
    elif xp_type==3:
        #Courbe parabolique
        result= 1.2*(lvl**3)-15*(lvl**2)+100*lvl-140
    else:
        #Courbe lente
        result= 1.25*(lvl**3)
    return int(result)+1
    
def get_next_level(xp,xp_type):
    '''
    return l'xp necessaire pour monter au niveau suivant
    '''
    return get_xp(get_level(xp,xp_type)+1,xp_type)-xp 
    
def gen_iv():
    '''
    genere les ivs d'une pokemon
    ivs[0] = For
    ivs[1] = Def
    ivs[2] = Vit
    ivs[3] = spe 
    '''
    ivs=[]
    for i in range(4):
        ivs.append(randint(0,15))
    pv=8*(ivs[0]%2)+4*(ivs[1]%2)+2*(ivs[2]%2)+1*(ivs[3]%2)
    ivs.append(pv)
    return ivs

def gen_ev():
    return [0 for i in range(5)]

def gen_stats(iv,ev,base_stats,xp):
    stats=[]
    lvl = get_level(xp,4)
    for i in range(5):
        iva = iv[i]
        base_stat = base_stats[i]
        eva = ev[i]
        if i<4:
            stat= (((iva+base_stat+((eva**0.5)/8))*lvl)/50)+5
            stats.append(stat)
        else:
            pv = (((iva+base_stat+((eva**0.5)/8)+50)*lvl)/50)+10
            stats.append(pv)
    return stats



ev = gen_ev()
iv = gen_iv()
xp = get_xp(100,4)
base_stats = [100,100,100,100,100]

print(get_level(352144,4))
print(get_xp(get_level(352144,3),4))
print(get_level(352144+get_next_level(352144,4),4))
print(gen_iv())
print(iv,ev,base_stats,xp)
print(gen_stats(iv,ev,base_stats,xp))