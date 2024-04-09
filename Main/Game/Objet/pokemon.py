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
    def __init__(self,data,lvl):
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
        self._xp = None
        self._lvl = lvl
        self._iv = None
        self._ev = None
        self._stats = None
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

    def get_base_xp(self):
        return self._base_xp
    
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
    
    def get_base_pv(self):
        return self._base_pv
    
    def get_base_for(self):
        return self._base_for
    
    def get_base_def(self):
        return self._base_def
    
    def get_base_vit(self):
        return self._base_vit
    
    def get_base_spe(self):
        return self._base_spe
    
    def get_capture_rate(self):
        return self._capture_rate

    def get_description(self):
        return self._description

    def set_surname(self,new_surname):
        """
        change le nom du pokemon.
        """
        self._surname = new_surname

    def get_surname(self):
        """
        Retourne le surnom du pokemon.
        """
        return self._surname
    
    def get_health_points(self):
        return self._healthPoints

    def get_level_from_xp(self):
        '''
        return le niveau du pokemon en fonction de son xp actuelle et de sa courbe d'xp
        '''
        xp = self.get_xp()
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
    
    def get_lvl(self):
        if self._xp == None and self._lvl == None:
            self._lvl = 1
        elif self._xp != None and self._lvl == None :
            self._xp = self.get_level_from_x(self._xp)
        return self._xp()
        
    def get_xp_from_lvl(self):
        '''
        return l'xp du pokemon en fonction d'un niveau donné et de sa courbe d'xp
        Cette methode sert uniquement a la generation d'un pokemon avec un niveau defini
        '''
        xp_type = self.get_nb_type_xp()
        lvl = self.get_level()
        base_xp = self.get_base_xp()
        if xp_type==1:
            #Courbe rapide
            result= base_xp+((lvl**3)*0.8)
        elif xp_type==2:
            #Courbe moyenne
            result= base_xp+(lvl**3)
        elif xp_type==3:
            #Courbe parabolique
            result= base_xp(1.2*(lvl**3)-15*(lvl**2)+100*lvl-140)
        else:
            #Courbe lente
            result= base_xp(1.25*(lvl**3))
        return int(result)
    
    def get_xp(self):
        if self._xp == None and self._lvl == None:
            self._xp = self.get_base_xp()
        elif self._xp == None and self._lvl != None :
            self._xp = self.get_xp_from_lvl(self._lvl)
        return self._xp()

    def get_next_level(self):
        '''
        return l'xp necessaire pour monter au niveau suivant
        '''
        xp = self.get_xp()
        xp_type = self.get_nb_type_xp()
        return self.get_xp(self.get_level(xp,xp_type)+1,xp_type)-xp

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
    
    def get_ivs(self):
        if self._iv == None:
            self._iv = self.gen_iv()
        return self._iv
    
    def gen_evs(self):
        return [0 for i in range(5)]
    
    def get_evs(self):
        if self._ev == None:
            self._ev = self.gen_evs()
        return self._ev

    def get_bases_stats(self):
        bases_stats=[]
        force = self.get_base_for()
        defence = self.get_base_def()
        vitesse = self.get_base_vit()
        special = self.get_base_spe()
        pvs = self.get_base_pv()
        bases_stats.append(force,defence,vitesse,special,pvs)
        return bases_stats

    def gen_stats(self):
        bases_stats = self.get_bases_stats()
        stats=[]
        lvl = self.get_level()
        for i in range(1,5):
            iv = self._iv[i]
            base_stat = bases_stats[i]
            ev = self._ev[i]
            if i<4:
                stat= (((iv+base_stat+((ev**0.5)/8))*lvl)/50)+5
                stats.append(stat)
            else:
                pv = (((iv+base_stat+((ev**0.5)/8)+50)*lvl)/50)+10
                stats.append(pv)
        return stats
    
    def get_stats(self):
        if self._stats == None:
            self._stats = self.gen_stats()
        return self._stats



