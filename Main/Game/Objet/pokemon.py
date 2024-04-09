from random import randint
import os
import pandas as pd
import requests

local_file = "Main/Game/Data/Pokémons.csv"
pokemons = pd.read_csv(local_file, delimiter = ",")


class Pokemon:
    """
    La classe d'un pokemon
    """
    def __init__(self,data,lvl = 2):
        self._id = ''
        self._pkd_id = ''
        self._name = ''
        self._shape = ''
        self._class = ''
        self._type = []
        self._base_xp = ''
        self._type_xp = ''
        self.evolution_lvl = ''
        self._height = ''
        self._weight = ''
        self._color = ''
        self._base_pv = ''
        self._base_for = ''
        self._base_def = ''
        self._base_vit = ''
        self._base_spe = ''
        self._capture_rate = ''
        self._description = ''
        self._surname = ''
        self._attaques = []
        self._xp = get_xp(lvl,xp_type)
        self._lvl = get_level(self._xp,xp_type)
        self._iv = gen_iv()
        self._ev = gen_ev()
        self._stats = []
        self._statut = None
        self._do = ""
        self._healthPoints = None

    
    def get_id(self):
        return self._id

    def get_pokedex_id(self):
        return self._pkd_id

    def get_name(self):
        return self._name
    
    def get_shape(self):
        return self._shape
    
    def get_class(self):
        return self._class
    
    def get_type(self):
        if len(self._type) == 2 :
            return self._type[0],self._type[1]
        else:
            return self._type[0]

    def get_type_xp(self):
        return self._type_xp
    
    def nb_type_xp(self):
        type_xp = self.get_type_xp()
        if type_xp == 'Slow':
            return 4
        elif type_xp == 'Medium Slow':
            return 3
        elif type_xp == 'Medium Fast':
            return 2 
        else:
            return 1
    
    def get_evolution_lvl(self):
        return self.evolution_lvl
    
    def get_height(self):
        return self._height
    
    def get_weight(self):
        return self._weight
    
    def get_color(self):
        return self._color


    def set_surname(self,new_name):
        """
        change le nom du pokemon.
        """
        self._surname = new_name

    def get_name(self):
        """
        Retourne le nom du pokemon.
        """
        return self._name
    
    def get_health_points(self):
        return self._healthPoints

    def get_level(self,xp):
        '''
        return le niveau du pokemon en fonction de son xp actuelle et de sa courbe d'xp
        '''
        i,lvl = 0,1
        xp_type = self.get_nb_type_xp()
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
    
    def get_next_level(self,xp):
        '''
        return l'xp necessaire pour monter au niveau suivant
        '''
        xp_type = self.get_nb_type_xp()
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
    
    def gen_stats(self):
        base_stat = get_base_stats()
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


