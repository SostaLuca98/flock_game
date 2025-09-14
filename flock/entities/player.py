from ..config import glob, opts
from .entity import Entity
import pygame, math, copy

class Player(Entity):

    def __init__(self, args, x: float, y: float, sprite_list, r: float) -> None:

        super(Player, self).__init__(args, r, sprite_list)
        
        # Define movement constants
        self.spe_c = self.args.speed
        self.acc_c = self.args.acc
        self.rot_c = self.args.rot

        # Define initial movement parameters
        self.tar_angle = 0
        self.dir_angle = 0
        self.speed = self.spe_c
        self.accel = 0

        # Define Position and Velocity
        self.x , self.y  = x, y
        self.vx, self.vy = self.spe_c, 0
        self.set_direction("E")

    def _move(self, dt) -> None:
        
        # Compute new velocity module
        self.speed += self.accel*dt
        self.speed = min(10*self.spe_c,max(self.spe_c/10, self.speed))

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

        # Update direction angle for rendering
        self.dir_angle = (math.atan2(-self.vy,self.vx)*360/(2*math.pi))%(360)

    def update(self, dt) -> None:
        super().update(dt)

    def render(self, screen: pygame.Surface) -> None:

        super().render(screen)
                
        for i in range(-1,2):
            for j in range(-1,2):
                cx, cy = self.x + i*glob.SW, self.y + j*glob.SH 
                r, w   = self.args.r, (1 if opts.mode==2 else 3)
                pygame.draw.circle(screen, (255,117,20), (cx*glob.SF,cy*glob.SF), r*glob.SF, w)

        if opts.scen != 3: return 
        self.draw_fullarrow(screen, (self.x, self.y),  
                            angle=self.dir_angle, 
                            color=(255,117,20), 
                            dims=(1.3*self.r*self.speed/self.spe_c,18,20))