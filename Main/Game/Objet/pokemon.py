from random import randint


class Pokemon:
    """
    La classe d'un pokemon
    """
    def __init__(self,id = 1,lvl = 2):
        self._id = id
        self._name = ''
        self._attaques = []
        self._xp = get_xp(lvl,xp_type)
        self._lvl = get_level(self._xp,xp_type)
        self._iv = gen_iv()
        self._ev = gen_ev()
        self._stats = []
        self._type = None
        self._do = ""
        self._healthPoints = None

    def __repr__(self):
        """
        methode spe qui represente le pokemon
        """
        return self.get_name()
            
    def set_name(self,new_name):
        """
        change le nom du pokemon.
        """
        self._name = new_name

    def get_name(self):
        """
        Retourne le nom du pokemon.
        """
        return self._name
    
    def get_health_points(self):
        return self._healthPoints

    def get_level(self,xp,xp_type):
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
        
    def get_xp(self,lvl,xp_type):
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
        return int(result)
    
    def get_next_level(self,xp,xp_type):
        '''
        return l'xp necessaire pour monter au niveau suivant
        '''
        return get_xp(get_level(xp,xp_type)+1,xp_type)-xp

    def gen_iv(self):
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
        return ivs.append(pv)
    
    def gen_ev(self):
        return [0 for i in range(5)]
    
    def gen_stats(self,get_base_stats()):
        stats=[]
        lvl = self._lvl
        for i in range(5):
            iv = self._iv[i]
            base_stat = base_stats[i]
            ev = self._ev[i]
            if i<4:
                stat= (((iv+base_stat+((ev**0.5)/8))*lvl)/50)+5
                stats.append(stat)
            else:
                pv = (((iv+base_stat+((ev**0.5)/8)+50)*lvl)/50)+10
                stats.append(pv)
        return stats

    def summary(self):
        summary = 'Nom:'+ self.get_name() + '\n' + '\n' + 'Points de vie:' + str(self.get_healthPoints())
        return summary

