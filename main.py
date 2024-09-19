from utils import SceneManager
from menu import MenuScene
from game import GameScene
import pygame, time

PAGE_WIDTH  = 1280
PAGE_HEIGHT = 720   

class Game:

    def __init__(self) -> None:
        """ Initialize global game variables """

        pygame.init() 
        self.running = True
        self.screen  = pygame.display.set_mode((PAGE_WIDTH, PAGE_HEIGHT))
        self.sprites = self.load_sprites()
        self.load_scenes()

    def load_scenes(self) -> None:
        self.scene_manager = SceneManager()
        scenes = {"game": GameScene(self.scene_manager, self.screen, self.sprites),
                  "menu": MenuScene(self.scene_manager, self.screen, self.sprites)}
        self.scene_manager.initialize(scenes, "game") # DI BASE ANDREBBE MENU


    def load_sprites(self) -> dict: 
        """ Load sprite textures into pygame as surfaces and returns a dictionary of names to surfaces. """
        
        sprites = {}
        sprites["ship"] = pygame.transform.rotate(pygame.image.load("gfx/ship.png").convert_alpha(),-90)
        # UCCELLO
        # PECORA
        # PESCE
        # BUFALO

        return sprites

    def run(self) -> None:
        """ Main Game Loop"""

        self.previous_time = time.time()
        while self.running:

            self.scene_manager.current_scene.poll_events()
            self.scene_manager.current_scene.update()
            self.scene_manager.current_scene.render()

            if self.scene_manager.quit == True:
                self.running = False    
        pygame.quit()

g = Game()
g.run()