import pygame, math, random
from .utils import SW, SH, SF

class NPC:

    def __init__(self, sprite: pygame.Surface) -> None:

        self.sprite = pygame.transform.scale_by(sprite, 0.05)
        
        self.rot_speed = 5
        self.tar_angle = random.random()*2*math.pi
        self.dir_angle = 0

        self.x = random.randint(int(self.sprite.get_size()[0]/2),int(SW-self.sprite.get_size()[0]/2))
        self.y = random.randint(int(self.sprite.get_size()[1]/2),int(SH-self.sprite.get_size()[1]/2))
        self.vx, self.vy = math.cos(self.tar_angle), math.sin(self.tar_angle)
        
        self.spe_c = 50
        self.acc_c = 300

        self.speed = self.spe_c
        self.accel = self.acc_c
        self.moving = True
        self.rect = self.sprite.get_rect()

    def update(self, dt) -> None:
        if self.moving: self.move(dt)

    def render(self, screen: pygame.Surface) -> None:
        rot_surf = pygame.transform.rotate(self.sprite,self.dir_angle)
        screen.blit(pygame.transform.scale_by(rot_surf, SF), ((self.x-rot_surf.get_size()[0]/2)*SF, (self.y-rot_surf.get_size()[1]/2)*SF))

    # def set_direction(self, player):
    #     dx = player.x-self.x
    #     dy = player.y-self.y
    #     self.tar_angle = (math.atan2(dy,dx)*360/(2*math.pi))%(360)

    def move(self, dt) -> None:
        
        self.vx += self.rot_speed*self.speed*math.cos(self.tar_angle)*dt
        self.vy += self.rot_speed*self.speed*math.sin(self.tar_angle)*dt
        vmod = math.sqrt(self.vx**2+self.vy**2)
        self.vx = self.vx/vmod*self.speed
        self.vy = self.vy/vmod*self.speed

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.x = self.x%SW
        self.y = self.y%SH


        self.dir_angle = (math.atan2(-self.vy,self.vx)*360/(2*math.pi))%(360)
