from .config import glob, args, opts
import pygame, math, copy

class Player:

    def __init__(self, args, x: float, y: float, sprite_list) -> None:

        self.args = copy.deepcopy(args)
        self.r = self.args.r_player

        if type(sprite_list) is not list: sprite_list = [sprite_list]
        self.sprite_list = [pygame.transform.scale_by(sprite, self.r/300) for sprite in sprite_list]
        self.sprite = self.sprite_list[0]
        self.sprite_index = 0
        self.sprite_count = 0
        
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

    def draw_fullarrow(self, angle: float, screen: pygame.Surface, color: tuple = (0, 0, 0)) -> None:
        arrow_length = self.args.r * 0.3 * glob.SF * self.speed/self.spe_c
        angle_rad = math.radians(-angle)
        start_pos = (self.x * glob.SF, self.y * glob.SF)
        end_pos = (
            start_pos[0] + arrow_length * math.cos(angle_rad),
            start_pos[1] + arrow_length * math.sin(angle_rad)
        )
        # Corpo della freccia (linea)
        pygame.draw.line(screen, color, start_pos, end_pos, 4)

        # Punta piena
        head_length = 18 * glob.SF
        head_width = 20 * glob.SF
        # Calcola i tre punti della punta
        tip = end_pos
        left = (
            tip[0] - head_length * math.cos(angle_rad) + head_width * math.sin(angle_rad) / 2,
            tip[1] - head_length * math.sin(angle_rad) - head_width * math.cos(angle_rad) / 2
        )
        right = (
            tip[0] - head_length * math.cos(angle_rad) - head_width * math.sin(angle_rad) / 2,
            tip[1] - head_length * math.sin(angle_rad) + head_width * math.cos(angle_rad) / 2
        )
        pygame.draw.polygon(screen, color, [tip, left, right])

    def change_sprite(self):
        self.sprite_count += 1
        if self.sprite_count > 4:
            self.sprite_count = 0
            self.sprite_index = (self.sprite_index + 1) % len(self.sprite_list)
            self.sprite = self.sprite_list[self.sprite_index]

    def update(self, dt) -> None:
        if self.moving: 
            self.change_sprite()
            self.move(dt)

    def render(self, screen: pygame.Surface) -> None:
        rot_surf = pygame.transform.rotate(self.sprite,self.dir_angle) 
        pygame.draw.circle(screen, (255,117,20), (self.x*glob.SF,self.y*glob.SF), self.args.r*glob.SF, width=(1 if opts.mode==2 else 3))
        screen.blit(pygame.transform.scale_by(rot_surf, glob.SF), ((self.x-rot_surf.get_size()[0]/2)*glob.SF, (self.y-rot_surf.get_size()[1]/2)*glob.SF))
        if opts.scen == 3: self.draw_fullarrow(self.dir_angle, screen, color=(255,117,20))

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