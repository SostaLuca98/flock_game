import pygame, math, random

class Block:

    def __init__(self, x: int, y: int, r: int, sprite: pygame.Surface) -> None:

        self.sprite = sprite
        #self.rect = self.sprite.get_rect()
        self.color = (255,0,0)
        
        self.x = x
        self.y = y
        self.r = r


    def update(self, dt) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r)

