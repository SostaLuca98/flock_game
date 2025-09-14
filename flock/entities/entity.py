from ..config import glob, opts
import pygame, random, math

class Entity:
    
    def __init__(self, args, r: float, sprite_list: pygame.Surface) -> None:

        self.args = args
        self.r = r

        # Render and Animation Sprites
        sprite_list = sprite_list if type(sprite_list) is list else [sprite_list]
        self._build_sprite(sprite_list, r, 1)

        # Moving Parameters
        self.moving = True
        self.dir_angle = 0.0
        self.tar_angle = 0.0

        # Position and Velocity
        self.x = random.randint(int(self.sprite.get_size()[0]/2),int(glob.SW-self.sprite.get_size()[0]/2))
        self.y = random.randint(int(self.sprite.get_size()[1]/2),int(glob.SH-self.sprite.get_size()[1]/2))
        self.vx, self.vy = math.cos(self.tar_angle), math.sin(self.tar_angle)

    def _build_sprite(self, sprite_list, radius, sprite_speed):

        self.sprite_index = 0
        self.sprite_count = 0
        self.sprite_speed = sprite_speed

        self.sprite_list = [pygame.transform.scale_by(sprite, radius/300) for sprite in sprite_list]
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

        self.x = self.x % glob.SW
        self.y = self.y % glob.SH
        
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
    
    def set_direction(self, direction):
        if   direction == "S": self.tar_angle = +math.pi/2
        elif direction == "N": self.tar_angle = -math.pi/2
        elif direction == "E": self.tar_angle = 0
        elif direction == "W": self.tar_angle = math.pi
    
    def set_speed(self, direction):
        if direction == "U": self.accel = +self.acc_c
        if direction == "D": self.accel = -self.acc_c
        if direction == "0": self.accel = 0
    
    @staticmethod
    def draw_fullarrow(screen, pos=(0,0), angle=0, color=(0,0,0), dims=(0,0,0)):

        arrow_length = dims[0] * glob.SF
        head_length  = dims[1] * glob.SF
        head_width   = dims[2] * glob.SF
        
        angle_rad = math.radians(-angle)
        start_pos = (pos[0] * glob.SF, pos[1] * glob.SF)
        end_pos = (start_pos[0] + arrow_length * math.cos(angle_rad),
                   start_pos[1] + arrow_length * math.sin(angle_rad))
        
        left  = (end_pos[0] - head_length * math.cos(angle_rad) + head_width * math.sin(angle_rad) / 2,
                 end_pos[1] - head_length * math.sin(angle_rad) - head_width * math.cos(angle_rad) / 2)
        right = (end_pos[0] - head_length * math.cos(angle_rad) - head_width * math.sin(angle_rad) / 2,
                 end_pos[1] - head_length * math.sin(angle_rad) + head_width * math.cos(angle_rad) / 2)

        pygame.draw.line(screen, color, start_pos, end_pos, 4)
        pygame.draw.polygon(screen, color, [end_pos, left, right])

        return