from ..config import glob, opts
import pygame

class Entity:
    
    def __init__(self, args, x: float, y: float, r: float, sprite_list: pygame.Surface) -> None:

        self.args = args
        self.r = r

        # Position and Velocity
        self.x,  self.y  =   x,   y
        self.vx, self.vy = 0.0, 0.0

        # Moving Parameters
        self.moving = True
        self.dir_angle = 0.0
        self.tar_angle = 0.0

        # Render and Animation Sprites
        sprite_list = sprite_list if type(sprite_list) is list else [sprite_list]
        self._build_sprite(sprite_list, 1)
        
    def _build_sprite(self, sprite_list, sprite_speed):

        self.sprite_index = 0
        self.sprite_count = 0
        self.sprite_speed = sprite_speed

        self.sprite_list = [pygame.transform.scale_by(sprite, self.r/300) for sprite in sprite_list]
        self.sprite = self.sprite_list[self.sprite_index]

        return

    def _change_sprite(self):

        self.sprite_count += 1
        if self.sprite_count <= self.sprite_speed: 
            return
        
        self.sprite_count = 0
        self.sprite_index = (self.sprite_index + 1) % len(self.sprite_list)
        self.sprite = self.sprite_list[self.sprite_index]

        return 

    def _move(self, dt) -> None:
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        return

    def update(self, dt) -> None:
        
        if self.moving: 
            self._change_sprite()
            self._move(dt)
        
        return

    def render(self, screen: pygame.Surface) -> None:
        
        surface = pygame.transform.rotate(self.sprite, self.dir_angle)
        center  = (self.x-surface.get_size()[0]/2)*glob.SF, (self.y-surface.get_size()[1]/2)*glob.SF
        screen.blit(pygame.transform.scale_by(surface, glob.SF), center)

        return