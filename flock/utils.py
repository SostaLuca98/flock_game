import pygame, time, random
FPS = 30
SW = 1280
SH = 720
SF = 1

class Button:
    def __init__(self,
                 x, y,
                 text: str) -> None:
        self.x = x*SF
        self.y = y*SF
        
        self.font = pygame.font.SysFont("Calibri", 36)
        self.color = "white"
        self.text = text

        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hovered = False

        self.event = lambda: print("Default button")

    def update(self, dt):
        if self.hovered is True:
            self.color = "blue"
        else:
            self.color = "white"

        self.text_surface = self.font.render(self.text, True, self.color)

    def set_hover(self, hovered: bool):
        self.hovered = hovered

    def register_event(self, func):
        self.event = func

    def render(self, screen: pygame.Surface):
        screen.blit(pygame.transform.scale_by(self.text_surface, SF), (self.x, self.y))

class SceneManager:

    def __init__(self) -> None:
        self.scenes = {}
        self.quit = False

    def initialize(self, scenes: dict, starting_scene: str) -> None:
        self.scenes = scenes
        self.current_scene = self.scenes[starting_scene]

    def set_scene(self, new_scene: str) -> None:
        self.current_scene = self.scenes[new_scene]

    def get_scene(self) -> None:
        return self.current_scene

    def quit_game(self) -> None:
        self.quit = True

class Scene:
    
    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:
        self.manager = manager # SceneManager to switch between scene and master things
        self.screen  = screen  # Blackboard for drawing
        self.tracker = tracker
        self.sprites = sprites # Collection of all png images for this scene
        self.previous_time = None

    def update_time(self):
        if self.previous_time is None: 
            self.previous_time = time.time()
        now = time.time()
        dt = now - self.previous_time
        while(dt<1/FPS):
            now = time.time()
            dt = now - self.previous_time
        self.previous_time = now
        return dt

    def update(self) -> None:
        pass

    def render(self) -> None:
        pass

    def poll_events(self) -> None:
        pass

