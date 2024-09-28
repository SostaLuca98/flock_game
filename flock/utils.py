from .config import glob, args, opts
import pygame, time, random

class Button:
    def __init__(self,
                 x, y,
                 text: str,
                 img: pygame.surface=None,
                 color = None) -> None:
        self.x = x
        self.y = y
        self.text = text
        self.hovered = False
        self.event = lambda: print("Default button")
        self.text_button = img is None
        self.fix_color = color

        if img is None: self.build_text()
        else: self.build_image(img)

        self.rect = self.surface.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def build_text(self):
        self.font = pygame.font.SysFont("Calibri", 72)
        self.color = "white" if self.fix_color is None else self.fix_color
        self.surface = self.font.render(self.text, True, self.color)
    def build_image(self, img):
        self.surface = img

    def update(self, dt):
        if self.text_button:
            if self.hovered: self.color = "blue"
            else: self.color = "white"
            self.color = "white" if self.fix_color is None else self.fix_color
            self.surface = self.font.render(self.text, True, self.color)

    def set_hover(self, hovered: bool):
        self.hovered = hovered

    def register_event(self, func):
        self.event = func
        return self

    def render(self, screen: pygame.Surface):
        new_surface = pygame.transform.scale_by(self.surface, glob.SF)
        screen.blit(new_surface, (self.x * glob.SF - new_surface.get_size()[0]/2, self.y * glob.SF - new_surface.get_size()[1]/2))

class SceneManager:

    def __init__(self) -> None:
        self.scenes = {}
        self.quit = False

    def initialize(self, scenes: dict, starting_scene: str) -> None:
        self.scenes = scenes
        self.current_scene = self.scenes[starting_scene]

    def set_scene(self, new_scene: str) -> None:
        self.scenes[new_scene].previous_time = None
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
        while(dt<1/glob.FPS):
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

