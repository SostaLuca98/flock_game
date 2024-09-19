import pygame, random

class NPC:

    def __init__(self, sprite: pygame.Surface) -> None:
        self.x = random.randint(0,1280)
        self.y = random.randint(0,720)
        self.sprite = pygame.transform.scale_by(sprite, 0.1)
        self.velocity = 500
        self.angle = 0
        self.direction = "N"
        self.moving = False
        self.rect = self.sprite.get_rect()

    def update(self, dt) -> None:
        if self.moving: self.move(dt)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))

    def set_direction(self, direction):
        self.direction = direction

    def move(self, dt) -> None:

        if   self.direction == "N": self.y -= self.velocity * dt
        elif self.direction == "S": self.y += self.velocity * dt
        elif self.direction == "W": self.x -= self.velocity * dt
        elif self.direction == "E": self.x += self.velocity * dt

        self.x = max(0,min(1280-self.rect.width,  self.x))
        self.y = max(0,min( 720-self.rect.height, self.y))