import pygame, math, random
from .utils import SF
from config import Params

class Block:

    def __init__(self, args, x: int, y: int, r: int, sprite: pygame.Surface) -> None:

        #self.rect = self.sprite.get_rect()
        self.color = (255,0,0)
        
        self.x = x
        self.y = y
        self.r = r
        self.sprite = pygame.transform.scale_by(sprite, 0.0042*self.r)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(pygame.transform.scale_by(self.sprite, SF), ((self.x-self.sprite.get_size()[0]/2)*SF, (self.y-self.sprite.get_size()[1]/2)*SF))
        #pygame.draw.circle(screen, self.color, (self.x,self.y), 3)
        #pygame.draw.circle(screen, self.color, (self.x+self.r,self.y), 3)

