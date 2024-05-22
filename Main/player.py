import pygame
import pytmx

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, map: map, x: int, y: int):
        super().__init__(keylistener, screen, x, y,color=map.current_map_color)
        self.pokedollars: int = 0

        self.map = map
        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.colors: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None
        self.current_map: Switch = Switch("switch", "chamber_0", pygame.Rect(0, 0, 0, 0), 0)

    def update(self) -> None:
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                temp_hitbox.x -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.check_collisions_colors(temp_hitbox)
                    self.move_left()
                else:
                    self.direction = "left"
            elif self.keylistener.key_pressed(pygame.K_d):
                temp_hitbox.x += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.check_collisions_colors(temp_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"
            elif self.keylistener.key_pressed(pygame.K_z):
                temp_hitbox.y -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.check_collisions_colors(temp_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"
            elif self.keylistener.key_pressed(pygame.K_s):
                temp_hitbox.y += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.check_collisions_colors(temp_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"


    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs
    
    def get_color_name(self, temp_hitbox: pygame.Rect) -> str:
        for color in self.colors:
            if temp_hitbox.colliderect(color.hitbox):
                return color.name
        return ""

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
        return None
    
    def add_collisions(self, collisions):
        self.collisions = collisions
    
    def add_color(self, color):
        self.colors = color
    
    def check_collisions_colors(self, temp_hitbox: pygame.Rect) -> bool:
        if self.colors: 
            for color in self.colors:
                if color.check_collision(temp_hitbox):
                    color_name = self.get_color_name(temp_hitbox)
                    if color_name != self.map.current_map_color:
                        self.map.hide_layer(color_name)
        return None
    
    def check_collisions(self, temp_hitbox: pygame.Rect):
        for collision in self.collisions:
            if temp_hitbox.colliderect(collision):
                return True
        return False