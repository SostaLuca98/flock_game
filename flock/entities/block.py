from .entity import Entity
import pygame

class Block(Entity):

    def __init__(self, x: int, y: int, r: int, sprite_list: pygame.Surface) -> None:

        super(Block, self).__init__(3*r, sprite_list)
        
        self.moving = False
        self.x, self.y = x, y
        self.r = r

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)