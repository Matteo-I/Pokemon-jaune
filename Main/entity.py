import pygame
from keylistener import KeyListener
from screen import Screen
from tool import Tool

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__()
        self.screen: Screen = screen
        self.keylistener: KeyListener = keylistener
        self.spritesheet: pygame.image = pygame.image.load("Main/Game/Data/sprites/characters/hero/red.png")
        self.image: pygame.image = Tool.split_image(self.spritesheet, 17, 1, 16, 16)
        self.position: pygame.math.Vector2 = pygame.math.Vector2(x +560, y+784)
        self.rect: pygame.Rect = self.image.get_rect()
        self.all_images: dict[str, list[pygame.image]] = self.get_all_images()
        self.index_image: int = 0
        self.image_part: int = 0
        self.reset_animation: bool = False
        self.hitbox: pygame.Rect = pygame.Rect(0, 0, 16, 12)

        self.step: int = 0
        self.animation_walk: bool = False
        self.direction: str = "down"

        self.animtion_step_time: float = 0.0
        self.action_animation: int = 5

    def update(self) -> None:
        self.animation_sprite()
        self.move()
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        self.image = self.all_images[self.direction][self.index_image]

    def move_left(self) -> None:
        self.animation_walk = True
        self.direction = "left"

    def move_right(self) -> None:
        self.animation_walk = True
        self.direction = "right"

    def move_up(self) -> None:
        self.animation_walk = True
        self.direction = "up"

    def move_down(self) -> None:
        self.animation_walk = True
        self.direction = "down"

    def animation_sprite(self) -> None:
        if int(self.step // 8) + self.image_part >= 4:
            self.image_part = 0
            self.reset_animation = True
        self.index_image = int(self.step // 8) + self.image_part

    def move(self) -> None:
        if self.animation_walk:
            self.animtion_step_time += self.screen.get_delta_time()
            if self.step < 16 and self.animtion_step_time >= self.action_animation:
                self.step += 1
                if self.direction == "left":
                    self.position.x -= 1
                elif self.direction == "right":
                    self.position.x += 1
                elif self.direction == "up":
                    self.position.y -= 1
                elif self.direction == "down":
                    self.position.y += 1
                self.animtion_step_time = 0
            elif self.step >= 16:
                self.step = 0
                self.animation_walk = False
                if self.reset_animation:
                    self.reset_animation = False
                else:
                    if self.image_part == 0:
                        self.image_part = 2
                    else:
                        self.image_part = 0

    def align_hitbox(self) -> None:
        self.position.x += 16
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.x % 16 != 0:
            self.rect.x -= 1
            self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.y % 16 != 0:
            self.rect.y -= 1
            self.hitbox.midbottom = self.rect.midbottom
        self.position = pygame.math.Vector2(self.rect.center)

    def get_all_images(self):
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }

        all_images["down"].append(Tool.split_image(self.spritesheet, 17, 0, 16, 16))
        all_images["down"].append(Tool.split_image(self.spritesheet, 0, 0, 16, 16))
        all_images["down"].append(Tool.split_image(self.spritesheet, 17, 0, 16, 16))
        all_images["down"].append(Tool.split_image(self.spritesheet, 34, 0, 16, 16))
        all_images["up"].append(Tool.split_image(self.spritesheet, 68, 0, 16, 16))
        all_images["up"].append(Tool.split_image(self.spritesheet, 51, 0, 16, 16))
        all_images["up"].append(Tool.split_image(self.spritesheet, 68, 0, 16, 16))
        all_images["up"].append(Tool.split_image(self.spritesheet, 85, 0, 16, 16))
        all_images["left"].append(Tool.split_image(self.spritesheet, 102, 0, 16, 16))
        all_images["left"].append(Tool.split_image(self.spritesheet, 119, 0, 16, 16))
        all_images["left"].append(Tool.split_image(self.spritesheet, 102, 0, 16, 16))
        all_images["left"].append(Tool.split_image(self.spritesheet, 119, 0, 16, 16))
        all_images["right"].append(Tool.split_image(self.spritesheet, 136, 0, 16, 16))
        all_images["right"].append(Tool.split_image(self.spritesheet, 153, 0, 16, 16))
        all_images["right"].append(Tool.split_image(self.spritesheet, 136, 0, 16, 16))
        all_images["right"].append(Tool.split_image(self.spritesheet, 153, 0, 16, 16))
        return all_images
        