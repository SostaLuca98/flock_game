import pygame, math, random

class NPC:

    def __init__(self, sprite: pygame.Surface) -> None:

        self.sprite = pygame.transform.scale_by(sprite, 0.1)
        
        self.x = random.randint(int(self.sprite.get_size()[0]/2),int(1280-self.sprite.get_size()[0]/2))
        self.y = random.randint(int(self.sprite.get_size()[1]/2),int( 720-self.sprite.get_size()[1]/2))
        self.vx, self.vy = 1, 0
        
        self.spe_c = 10
        self.acc_c = 300
        
        self.rot_speed = 10
        self.tar_angle = 0
        self.dir_angle = 0

        self.speed = self.spe_c
        self.accel = self.acc_c
        self.moving = True
        self.rect = self.sprite.get_rect()

    def update(self, dt) -> None:
        if self.moving: self.move(dt)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def render(self, screen: pygame.Surface) -> None:
        rot_surf = pygame.transform.rotate(self.sprite,self.dir_angle) 
        screen.blit(rot_surf, (self.x-rot_surf.get_size()[0]/2, self.y-rot_surf.get_size()[1]/2))

    def set_direction(self, player):
        dx = player.x-self.x
        dy = player.y-self.y
        self.tar_angle = (math.atan2(dy,dx)*360/(2*math.pi))%(360)

    def move(self, dt) -> None:

        self.speed += self.accel*dt
        self.speed = min(10*self.spe_c,max(self.spe_c/10, self.speed))
        
        self.vx += self.rot_speed*self.speed*math.cos(self.tar_angle)*dt
        self.vy += self.rot_speed*self.speed*math.sin(self.tar_angle)*dt
        vmod = math.sqrt(self.vx**2+self.vy**2)
        self.vx = self.vx/vmod*self.speed
        self.vy = self.vy/vmod*self.speed

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = max(self.rect.width/2 ,min(1280-self.rect.width/2,  self.x))
        self.y = max(self.rect.height/2,min( 720-self.rect.height/2, self.y))

        self.dir_angle = (-math.atan2(self.vy,self.vx)*360/(2*math.pi))%(360)