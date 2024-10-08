from .config import glob, args, opts
import pygame, math, copy

class Player:

    def __init__(self, args, x: float, y: float, sprite: pygame.Surface) -> None:

        self.args = copy.deepcopy(args)
        self.r = self.args.r_player
        self.sprite = pygame.transform.scale_by(sprite, self.r/300)
        
        self.spe_c = self.args.speed
        self.acc_c = self.args.acc
        self.rot_c = self.args.rot

        self.x , self.y  = x, y
        self.vx, self.vy = self.spe_c, 0

        self.tar_angle = 0
        self.dir_angle = 0

        self.accel = 0
        self.speed = self.spe_c

        self.set_direction("E")
        self.moving = True
        self.rect = self.sprite.get_rect()

    def update(self, dt) -> None:
        if self.moving: self.move(dt)

    def render(self, screen: pygame.Surface) -> None:
        rot_surf = pygame.transform.rotate(self.sprite,self.dir_angle) 
        pygame.draw.circle(screen, (255,117,20), (self.x*glob.SF,self.y*glob.SF), self.args.r*glob.SF, width=3)
        screen.blit(pygame.transform.scale_by(rot_surf, glob.SF), ((self.x-rot_surf.get_size()[0]/2)*glob.SF, (self.y-rot_surf.get_size()[1]/2)*glob.SF))

    def set_direction(self, direction):
        if   direction == "S": self.tar_angle = +math.pi/2
        elif direction == "N": self.tar_angle = -math.pi/2
        elif direction == "E": self.tar_angle = 0
        elif direction == "W": self.tar_angle = math.pi
    
    def set_speed(self, direction):
        if direction == "U": self.accel = +self.acc_c
        if direction == "D": self.accel = -self.acc_c
        if direction == "0": self.accel = 0

    def move(self, dt) -> None:

        self.speed += self.accel*dt
        self.speed = min(10*self.spe_c,max(self.spe_c/10, self.speed))
        
        self.vx += self.rot_c * self.speed * math.cos(self.tar_angle) * dt
        self.vy += self.rot_c * self.speed * math.sin(self.tar_angle) * dt
        vmod = math.sqrt(self.vx**2+self.vy**2)
        self.vx = self.vx/vmod*self.speed
        self.vy = self.vy/vmod*self.speed

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = self.x%glob.SW
        self.y = self.y%glob.SH

        self.dir_angle = (math.atan2(-self.vy,self.vx)*360/(2*math.pi))%(360)