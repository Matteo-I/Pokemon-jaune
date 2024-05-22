import pygame


class Switch:
    def __init__(self, type: str, name: str, hitbox: pygame.Rect, port: int, color_name: str | None = None ):
        self.type = type
        self.name = name
        self.hitbox = hitbox
        self.port = port
        self.color_name = color_name

    def check_collision(self, temp_hitbox):
        return self.hitbox.colliderect(temp_hitbox)
    
    def get_name(self):
        return self.name

    def get_port(self):
        return self.port
