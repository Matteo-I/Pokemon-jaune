import pygame
import pyscroll
import pytmx

from player import Player
from screen import Screen
from switch import Switch

class Map:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None

        
        self.player: Player | None = None
        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.colors: list[pygame.Rect] | None = None
        
        self.current_map: Switch = Switch("switch", "chamber_0", pygame.Rect(0, 0, 0, 0), 0)
        self.current_map_name: str = ""
        self.color_list= ['purple','green']
        self.current_map_color: str = "purple"

        self.switch_map(self.current_map)

    def switch_map(self, switch: Switch) -> None:
        self.tmx_data = pytmx.load_pygame(f"Main/Game/Map/{switch.get_name()}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=9)

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in self.color_list and layer.name.split(' ')[-1] != self.current_map_color:
                layer.visible = False
            elif layer.name.split(' ')[-1] == self.current_map_color:
                layer.visible = True

        self.map_layer.zoom = 3

        self.switchs = []
        self.collisions = []
        self.colors = []

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            type = str(obj.name).split(" ")[0]
            if type == "switch":
                self.switchs.append(Switch(
                    type, str(obj.name).split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height), int(obj.name.split(" ")[-1])
                ))
            if str(obj.name).split(' ')[0] == 'color':
                color_name = str(obj.name).split(' ')[1]
                self.colors.append(Switch("color", color_name, pygame.Rect(obj.x, obj.y, obj.width, obj.height), 0, color_name))

        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collisions(self.collisions)
            self.player.add_color(self.colors)
            self.group.add(self.player)

        self.current_map = switch
        self.current_map_name = switch.get_name()


    def add_player(self, player) -> None:
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.collisions)

    def hide_layer(self, layer_name: str) -> None:
        self.current_map_color = layer_name
        tmx_file = f"Main/Game/Map/{self.current_map_name}.tmx"
        tmx_data = pytmx.load_pygame(tmx_file)
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in self.color_list and layer.name != layer_name:
                layer.visible = False
            elif layer.name.split(' ')[-1] == layer_name:
                layer.visible = True

        self.recharge_map(tmx_data)

        if self.player:
            self.player.change_color(layer_name)

    
    def recharge_map(self,data):
        tmx_data = data
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=9)

        self.map_layer.zoom = 3
        if self.player:
            self.group.add(self.player)
            self.group.center((self.player.rect.center[0]+8, self.player.rect.center[1]+4))
        self.group.draw(self.screen.get_display())

    
    def update(self) -> None:
        if self.player:
            if self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None
        self.group.update()
        self.group.center((self.player.rect.center[0]+8,self.player.rect.center[1]+4))
        self.group.draw(self.screen.get_display())

    def pose_player(self, switch: Switch):
        position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)