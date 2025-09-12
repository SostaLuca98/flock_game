from ..config import glob, args, opts
from .entity import Entity
import pygame, math, random, copy

class NPC(Entity):

    def __init__(self, args, sprite_list: pygame.Surface, r: float) -> None:

        super(NPC, self).__init__(args, r, sprite_list)

        # Define movement constants
        self.arrived = False
        self.spe_c = self.args.speed
        self.acc_c = 0
        self.rot_c = 5

        # Define initial movement parameters
        self.tar_angle = random.random()*2*math.pi
        self.dir_angle = 0
        self.speed = self.spe_c
        self.accel = 0

        # Define Position and Velocity
        self.x = random.randint(int(self.sprite.get_size()[0]/2),int(glob.SW-self.sprite.get_size()[0]/2))
        self.y = random.randint(int(self.sprite.get_size()[1]/2),int(glob.SH-self.sprite.get_size()[1]/2))
        self.vx, self.vy = math.cos(self.tar_angle), math.sin(self.tar_angle)

    def _move(self, dt) -> None:
        
        # Compute new velocity components
        self.vx += self.rot_c*self.speed*math.cos(self.tar_angle)*dt
        self.vy += self.rot_c*self.speed*math.sin(self.tar_angle)*dt
        
        # Normalize velocity to current speed
        vmod = math.sqrt(self.vx**2+self.vy**2)
        self.vx = self.vx/vmod*self.speed
        self.vy = self.vy/vmod*self.speed

        # Update position with toroidal boundary conditions
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = self.x % glob.SW
        self.y = self.y % glob.SH

        # Check if arrived
        if self.arrived:
            print("wyiuajed")
            self.x, self.y = 1e4, 1e4
            self.moving = False

        # Update direction angle for rendering
        self.dir_angle = (math.atan2(-self.vy,self.vx)*360/(2*math.pi))%(360)

    def update(self, dt) -> None:
        super().update(dt)

    def render(self, screen: pygame.Surface) -> None:
        
        super().render(screen)
        
        if opts.scen != 3: return 
        self.draw_fullarrow(screen, (self.x, self.y), 
                            angle=self.dir_angle, 
                            color=(0,0,0), 
                            dims=(0.7*self.r,10,15))