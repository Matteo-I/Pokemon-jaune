
class Pokemon:
    """
    La classe d'un pokemon
    """
    def __init__(self, name):
        self._name = name
        self._attaques = []
        self._xp = 0
        self._iv = []
        self._type = None
        self._do = ""
        self._healthPoints = None

    def __repr__(self):
            """
            methode spe qui represente le pokemon
            """
            return self.get_name()
            
    def get_name(self):
        """
        Retourne le nom du pokemon.
        """
        return self._name
    
    def get_healthPoints(self):
        return self._healthPoints

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
    
    def get_next_level(xp,xp_type):
        lvl= get_level(xp,xp_type)
        

        

    def summary(self):
        summary = 'Nom:'+ self.get_name() + '\n' + '\n' + 'Points de vie:' + str(self.get_healthPoints())
        return summary

