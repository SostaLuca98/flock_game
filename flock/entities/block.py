from ..config import glob, args, opts
from .entity import Entity
import pygame, math, random, copy

class Block(Entity):

    def __init__(self, args, x: int, y: int, r: int, sprite_list: pygame.Surface) -> None:

        super(Block, self).__init__(args, 3*r, sprite_list)
        
        self.moving = False
        self.x, self.y = x, y
        self.r = r

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)