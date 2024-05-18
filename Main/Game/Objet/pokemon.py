from random import randint
import os
import pandas as pd
#sqlalchemy import
from typing import List,Optional
from sqlalchemy import ForeignKey,String,Integer,Float,select,create_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,Session


class Base(DeclarativeBase):
    pass

class Monster(Base):
    __tablename__ = "POKEMON"

    id: Mapped[int] = mapped_column(primary_key=True)
    nb_pokedex: Mapped[int] = mapped_column(Integer)
    nom: Mapped[str] = mapped_column(String(12))
    forme: Mapped[str] = mapped_column(String(10))
    classification: Mapped[str] = mapped_column(String(15))
    type_1: Mapped[str] = mapped_column(String(10))
    type_2: Mapped[Optional[str]] = mapped_column(String(10))
    base_xp: Mapped[int] = mapped_column(Integer)
    type_xp: Mapped[str] = mapped_column(String(15))
    evolution_lvl: Mapped[Optional[int]] = mapped_column(Integer)
    taille: Mapped[int] = mapped_column(Float)
    poids: Mapped[int] = mapped_column(Float)
    couleur: Mapped[str] = mapped_column(String(10))
    pv: Mapped[int] = mapped_column(Integer)
    force: Mapped[int] = mapped_column(Integer)
    defence: Mapped[int] = mapped_column(Integer)
    vitesse: Mapped[int] = mapped_column(Integer)
    special: Mapped[int] = mapped_column(Integer)
    taux_capture: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(String(250))

    def __repr__(self) -> str:
        # return f"Pokemon(id={self.id!r}, name={self.name!r})"
        return dir(self)
    
class Monster_save(Base):
    __tablename__ = "POKEMON_SAVED"

    id_save: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(Integer)
    surnom: Mapped[str] = mapped_column(String(12))
    attaque_1_id: Mapped[Optional[int]] = mapped_column(Integer)
    attaque_2_id: Mapped[Optional[int]] = mapped_column(Integer)
    attaque_3_id: Mapped[Optional[int]] = mapped_column(Integer)
    attaque_4_id: Mapped[Optional[int]] = mapped_column(Integer)
    xp: Mapped[int] = mapped_column(Integer)
    iv_pv: Mapped[int] = mapped_column(Integer)
    iv_force: Mapped[int] = mapped_column(Integer)
    iv_defence: Mapped[int] = mapped_column(Integer)
    iv_vitesse: Mapped[int] = mapped_column(Integer)
    iv_special: Mapped[int] = mapped_column(Integer)
    ev_pv: Mapped[int] = mapped_column(Integer)
    ev_force: Mapped[int] = mapped_column(Integer)
    ev_defence: Mapped[int] = mapped_column(Integer)
    ev_vitesse: Mapped[int] = mapped_column(Integer)
    ev_special: Mapped[int] = mapped_column(Integer)
    statut: Mapped[Optional[str]] = mapped_column(String(12))
    do: Mapped[Optional[str]] = mapped_column(String(12))
    pv: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        # return f"Pokemon(id={self.id!r}, name={self.name!r})"
        return dir(self)

sql_data="Main/Game/Data/ressources/pokemon.db"
csv_data = "Main/Game/Data/ressources/Pokemons.csv"
engine = create_engine(f"sqlite:///{sql_data}", echo=False)
pokemons_datas = pd.read_csv(csv_data, delimiter = ",")

def replace(nb):
    if isinstance(nb,float) or isinstance(nb,int):
        return float(nb)
    elif ',' in nb :
        nb = nb.replace(',','.')
        return float(nb)
    else:
        return float(nb)

def check(val):
    if isinstance(val,int) or isinstance(val,float) and val > 0:
        return int(val)
    elif isinstance(val,str):
        return replace(val)
    else:
        return 0

def create_sql_database(pokemons_datas):
    for i in range(len(pokemons_datas)):
        with Session(engine) as session:
            Poke = Monster(
            id=pokemons_datas.values[i][0],
            nb_pokedex=pokemons_datas.values[i][1],
            nom=pokemons_datas.values[i][2],
            forme=pokemons_datas.values[i][3],
            classification=pokemons_datas.values[i][4],
            type_1=pokemons_datas.values[i][5],
            type_2=pokemons_datas.values[i][6],
            base_xp=pokemons_datas.values[i][7],
            type_xp=pokemons_datas.values[i][8],
            evolution_lvl=pokemons_datas.values[i][9],
            taille=replace(pokemons_datas.values[i][10]),
            poids=check(pokemons_datas.values[i][11]),
            couleur=pokemons_datas.values[i][12],
            pv=pokemons_datas.values[i][13],
            force=pokemons_datas.values[i][14],
            defence=pokemons_datas.values[i][15],
            vitesse=pokemons_datas.values[i][16],
            special=pokemons_datas.values[i][17],
            taux_capture=pokemons_datas.values[i][18],
            description=pokemons_datas.values[i][19],
            )
        session.add_all([Poke])
        session.commit()    

if not "pokemon.db" in os.listdir('Main/Game/Data/ressources'):
    Base.metadata.create_all(engine)
    create_sql_database(pokemons_datas)


class Pokemon():
    """
    La classe d'un pokemon
    """
    def __init__(self,id,surname = None, attaques = [],xp = None,iv = None,ev = None,statut = None,do = None,pv = 0):
        self.id = id
        self._do = do
        self._healthPoints = pv
        self._surname = surname if surname is not None else self.name
        self._attaques = attaques
        self._statut = statut
        self._pkd_id = self.get_pokedex_id()
        self.name = self.get_name()
        self._shape = self.get_shape()
        self._class = self.get_class()
        self._type = self.get_type()
        self._base_xp = self.get_base_xp()
        self._type_xp = self.get_type_xp()
        self._evolution_lvl = self.get_evolution_lvl()
        self._height = self.get_height()
        self._weight = self.get_weight()
        self._color = self.get_color()
        self._base_pv = self.get_base_pv()
        self._base_for = self.get_base_for()
        self._base_def = self.get_base_def()
        self._base_vit = self.get_base_vit()
        self._base_spe = self.get_base_spe()
        self._base_capture_rate = self.get_base_capture_rate()
        self._description = self.get_description()
        self._xp = xp if xp is not None else self.get_base_xp()
        self._lvl = self.get_level_from_xp()
        self._iv = iv if iv is not None else self.gen_iv()
        self._ev = ev if ev is not None else self.gen_evs()
        self._stats = self.gen_stats()
        self._capture_rate = self.get_capture_rate()
        

    def get_id(self):
        return self.id

    def get_pokedex_id(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.nb_pokedex).where(Monster.id == self.id))

    def get_name(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.nom).where(Monster.id == self.id))
    
    def get_shape(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.forme).where(Monster.id == self.id))
    
    def get_class(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.classification).where(Monster.id == self.id))
    
    def get_type(self):
        with Session(engine) as session:
            return [session.scalar(select(Monster.type_1).where(Monster.id == self.id)),session.scalar(select(Monster.type_2).where(Monster.id == self.id))]

    def get_base_xp(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.base_xp).where(Monster.id == self.id))
    
    def get_type_xp(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.type_xp).where(Monster.id == self.id))
    
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
        with Session(engine) as session:
            return session.scalar(select(Monster.evolution_lvl).where(Monster.id == self.id))
    
    def get_height(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.taille).where(Monster.id == self.id))
    
    def get_weight(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.poids).where(Monster.id == self.id))
        
    
    def get_color(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.couleur).where(Monster.id == self.id))
    
    def get_base_pv(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.pv).where(Monster.id == self.id))
    
    def get_base_for(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.force).where(Monster.id == self.id))
    
    def get_base_def(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.defence).where(Monster.id == self.id))
    
    def get_base_vit(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.vitesse).where(Monster.id == self.id))
    
    def get_base_spe(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.special).where(Monster.id == self.id))
    
    def get_base_capture_rate(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.taux_capture).where(Monster.id == self.id))

    def get_description(self):
        with Session(engine) as session:
            return session.scalar(select(Monster.description).where(Monster.id == self.id))
        
    def get_capture_rate(self, ball=None):
        ball_bonus = {
            'pokeball': 1,
            'greatball': 1.5,
            'safariball' : 1.5,
            'ultraball': 2,
        }

        bonus_statut = 0
        statut = self.get_statut()
        if statut in ['bruler', 'poison', 'paralyser']:
            bonus_statut = 1
        elif statut in ['sommeil', 'geler']:
            bonus_statut = 2

        if ball is None or ball not in ball_bonus:
            bonus_ball = 1
            if ball == 'masterball':
                return 100
        else:
            bonus_ball = ball_bonus[ball]
            

        # Formule de capture de Pokémon Jaune
        capture_rate = ((3 * self.get_pv() - 2 * self.get_health_points()) * min((self.get_base_capture_rate() * 2.95 * bonus_ball),752) / (3 * self.get_pv())) * max((5.75 *bonus_statut),1)
        # Limite le taux de capture à 100%
        self._capture_rate = min(round(capture_rate/10, 2), 100)
        return self._capture_rate


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
    
    def set_do(self,dresseur):
        """
        change le nom du pokemon.
        """
        self._do = dresseur

    def set_statut(self,statut):
        """
        change le nom du pokemon.
        """
        self._statut = statut
    
    def get_statut(self):
        return self._statut

    def get_do(self):
        """
        Retourne le surnom du pokemon.
        """
        return self._do
    
    def get_health_points(self):
        return self._healthPoints
    
    def heal(self,nb):
        self._healthPoints += nb
        if self._healthPoints > self.get_pv():
            self._healthPoints = self.get_pv()
        self._healthPoints = self.get_health_points()
        self._capture_rate = self.get_base_capture_rate
    
    def damage(self,nb):
        self._healthPoints -= nb
        if self._healthPoints < 0:
            self._healthPoints = 0
        self._healthPoints = self.get_health_points()
        self._capture_rate = self.get_base_capture_rate
    
    def get_attaque(self):
        return self._attaques
            

    def get_level_from_xp(self):
        '''
        return le niveau du pokemon en fonction de son xp actuelle et de sa courbe d'xp
        '''
        xp = self.get_xp()-self.get_base_xp()
        i,lvl = 0,1
        xp_type = self.nb_type_xp()
        if xp_type==1:
            #Courbe rapide
            while i<xp:
                lvl+=1
                i=(lvl**3)*0.8
            return lvl
        elif xp_type==2:
            #Courbe moyenne
            while i<xp:
                lvl+=1
                i=lvl**3
            return lvl
        elif xp_type==3:
            #Courbe parabolique
            while i<xp:
                lvl+=1
                i=1.2*(lvl**3)-15*(lvl**2)+100*lvl-140
            return lvl
        else:
            #Courbe lente
            while i<xp:
                lvl+=1
                i=1.25*(lvl**3)
            return lvl
    
    def get_lvl(self):
        return self._lvl
        
    def get_xp_from_lvl(self,lvl):
        '''
        return l'xp du pokemon en fonction d'un niveau donné et de sa courbe d'xp
        Cette methode sert uniquement a la generation d'un pokemon avec un niveau defini
        '''
        xp_type = self.nb_type_xp()
        base_xp = self.get_base_xp()
        if xp_type==1:
            #Courbe rapide
            result= base_xp+((lvl**3)*0.8)
        elif xp_type==2:
            #Courbe moyenne
            result= base_xp+(lvl**3)
        elif xp_type==3:
            #Courbe parabolique
            result= base_xp+(1.2*(lvl**3)-15*(lvl**2)+100*lvl-140)
        else:
            #Courbe lente
            result= base_xp+(1.25*(lvl**3))
        return int(result)
    
    def get_xp(self):
        return self._xp

    def get_next_level(self):
        '''
        return l'xp necessaire pour monter au niveau suivant
        '''
        if self.get_lvl() == 100:
            return 0
        xp = self.get_xp()
        return self.get_xp_from_lvl(self.get_lvl()+1)-xp
    
    def add_xp(self,nb):
        self._xp += nb
        pre_pv = self.get_pv()
        pre_hp = float(self.get_health_points())
        print(pre_hp,pre_pv)
        if self._xp > self.get_xp_from_lvl(100):
            self._xp = self.get_xp_from_lvl(100)
        self._lvl = self.get_level_from_xp()
        self._stats = self.gen_stats()
        self._healthPoints= (((pre_hp*100)/pre_pv)/100)*self.get_pv()

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
        ivs.append(pv)
        return ivs
    
    def get_ivs(self):
        return self._iv

    def get_iv_for(self):
        iv = self.get_ivs()[0]
        return iv
    
    def get_iv_def(self):
        iv = self.get_ivs()[1]
        return iv

    def get_iv_vit(self):
        iv = self.get_ivs()[2]
        return iv
    
    def get_iv_spe(self):
        iv = self.get_ivs()[3]
        return iv

    def get_iv_pv(self):
        iv = self.get_ivs()[4]
        return iv
    
    def gen_evs(self):
        return [0 for i in range(5)]
    
    def get_evs(self):
        return self._ev
    
    def get_ev_for(self):
        ev = self.get_evs()[0]
        return ev
    
    def get_ev_def(self):
        ev = self.get_evs()[1]
        return ev

    def get_ev_vit(self):
        ev = self.get_evs()[2]
        return ev
    
    def get_ev_spe(self):
        ev = self.get_evs()[3]
        return ev

    def get_ev_pv(self):
        ev = self.get_evs()[4]
        return ev
    
    def add_ev_for(self,nb):
        ev = self.get_ev_for()
        ev += nb
        if ev >= 65535:
            ev = 65535
        self._ev[0] = ev
        self._stats = self.gen_stats()
    
    def add_ev_def(self,nb):
        ev = self.get_ev_def()
        ev += nb
        if ev >= 65535:
            ev = 65535
        self._ev[1] = ev
        self._stats = self.gen_stats()
    
    def add_ev_vit(self,nb):
        ev = self.get_ev_vit()
        ev += nb
        if ev >= 65535:
            ev = 65535
        self._ev[2] = ev
        self._stats = self.gen_stats()
        
    
    def add_ev_spe(self,nb):
        ev = self.get_ev_spe()
        ev += nb
        if ev >= 65535:
            ev = 65535
        self._ev[3] = ev
        self._stats = self.gen_stats()

    def add_ev_pv(self,nb):
        ev = self.get_ev_pv()
        ev += nb
        if ev >= 65535:
            ev = 65535
        self._ev[4] = ev
        self._stats = self.gen_stats()
    
    def get_bases_stats(self):
        force = self.get_base_for()
        defence = self.get_base_def()
        vitesse = self.get_base_vit()
        special = self.get_base_spe()
        pvs = self.get_base_pv()
        return [force,defence,vitesse,special,pvs]

    def gen_stats(self):
        bases_stats = self.get_bases_stats()
        stats=[]
        lvl = self.get_lvl()
        for i in range(0,5):
            iv = self.get_ivs()[i]
            base_stat = bases_stats[i]
            ev = self.get_evs()[i]
            if i<4:
                stat= (((iv+base_stat+((ev**0.5)/8))*lvl)/50)+5
                stats.append(stat)
            else:
                pv = (((iv+base_stat+((ev**0.5)/8)+50)*lvl)/50)+10
                stats.append(pv)
        return stats
    
    def get_stats(self):
        return self._stats
    
    def get_for(self):
        force = self.get_stats()[0]
        return force
    
    def get_def(self):
        defence = self.get_stats()[1]
        return defence

    def get_vit(self):
        vitesse = self.get_stats()[2]
        return vitesse
    
    def get_spe(self):
        special = self.get_stats()[3]
        return special

    def get_pv(self):
        pv = self.get_stats()[4]
        return pv
    
    def save_pokemon(self):
        
        
        pass
    
    def __repr__(self) -> str:
        return (f"Pokemon("f"id={self.get_id()}\n,"
          f"name={self.get_name()}\n,"
          f"surnamename={self.get_surname()}\n,"
          f"index pokedex={self.get_pokedex_id()}\n,"
          f"shape={self.get_shape()}\n,"
          f"classification={self.get_class()}\n,"
          f"height={self.get_height()}\n,"
          f"weight={self.get_weight()}\n,"
          f"color={self.get_color()}\n,"
          f"description={self.get_description()}\n,"
          f"do={self.get_do()}\n,"
          f"type={self.get_type()}\n,"
          f"xp={self.get_xp()}\n,"
          f"base xp ={self.get_base_xp()}\n,"
          f"xp type={self.get_type_xp()}\n,"
          f"level ={self.get_lvl()}\n,"
          f"xp to next level={self.get_next_level()}\n,"
          f"level evolution={self.get_evolution_lvl()}\n,"
          f"attaque={self.get_attaque()}\n,"
          f"base capture rate={self.get_base_capture_rate()}\n,"
          f"capture rate={self.get_capture_rate()}\n,"
          f"base stats={self.get_bases_stats()}\n,"
          f"stats={self.get_stats()}\n,"
          f"iv={self.get_ivs()}\n,"
          f"ev={self.get_evs()}\n,"
          f"health={self.get_health_points()}\n,"
          f"statut={self.get_statut()})")
    
pokemon = Pokemon(84,'poketest', [],660451,[15,15,15,15,15],None,None,"Dev",150)
print(pokemon)
pokemon.add_xp(200000)
print(pokemon.get_health_points())


