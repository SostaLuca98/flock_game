import pygame, time, random

class Entity:

    def __init__(self) -> None:
        pass

    def update(self, dt) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass

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
    
    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict) -> None:
        self.manager = manager # SceneManager to switch between scene and master things
        self.screen  = screen  # Blackboard for drawing
        self.sprites = sprites # Collection of all png images for this scene
        self.previous_time = None

    def update_time(self):
        if self.previous_time is None: 
            self.previous_time = time.time()
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

