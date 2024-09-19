import pygame, math

class Player:

    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:

        self.sprite = pygame.transform.scale_by(sprite, 0.3)
        
        self.x , self.y  = x, y
        self.vx, self.vy = 100, 0
        self.speed = 60
        self.acceleration = self.speed 
        self.tar_angle = 0
        self.dir_angle = 0

        self.direction = "E"
        self.moving = False
        self.rect = self.sprite.get_rect()

    def update(self, dt) -> None:
        if self.moving: self.move(dt)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def render(self, screen: pygame.Surface) -> None:
        rot_surf = pygame.transform.rotate(self.sprite,self.dir_angle) 
        screen.blit(rot_surf, (self.x-rot_surf.get_size()[0]/2, self.y-rot_surf.get_size()[1]/2))

    def set_direction(self, direction):
        self.direction = direction

    def move(self, dt) -> None:

        if   self.direction == "S": self.tar_angle = +math.pi/2
        elif self.direction == "N": self.tar_angle = -math.pi/2
        elif self.direction == "E": self.tar_angle = 0
        elif self.direction == "W": self.tar_angle = math.pi
        
        self.vx += self.acceleration*math.cos(self.tar_angle)*dt
        self.vy += self.acceleration*math.sin(self.tar_angle)*dt
        vmod = math.sqrt(self.vx**2+self.vy**2)
        self.vx = self.vx/vmod*self.speed
        self.vy = self.vy/vmod*self.speed

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = max(self.rect.width/2 ,min(1280-self.rect.width/2,  self.x))
        self.y = max(self.rect.height/2,min( 720-self.rect.height/2, self.y))

        self.dir_angle = (-math.atan2(self.vy,self.vx)*360/(2*math.pi))%(360)