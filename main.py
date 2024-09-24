from flock import SceneManager, MenuScene, GameScene, Tracker
from flock import SW, SH, SF
import pygame, time

TRACKER_FLAG = False

class Game:

    def __init__(self) -> None:
        """ Initialize global game variables """

        pygame.init() 
        self.running = True
        self.screen  = pygame.display.set_mode((int(SW*SF), int(SH*SF)))
        self.tracker = Tracker() if TRACKER_FLAG else None
        self.sprites = self.load_sprites()
        self.load_scenes()

    def load_scenes(self) -> None:
        self.scene_manager = SceneManager()
        scenes = {"game": GameScene(self.scene_manager, self.screen, self.tracker, self.sprites, "birds"),
                  "menu": MenuScene(self.scene_manager, self.screen, self.tracker, self.sprites)}
        self.scene_manager.initialize(scenes, "game") # DI BASE ANDREBBE MENU


    def load_sprites(self) -> dict: 
        """ Load sprite textures into pygame as surfaces and returns a dictionary of names to surfaces. """
        
        sprites = {}
        sprites["ship"] = pygame.transform.rotate(pygame.image.load("gfx/ship.png").convert_alpha(),-90)
        sprites["birdL"] = pygame.transform.rotate(pygame.image.load("gfx/birdL.png").convert_alpha(),225)
        sprites["birdN"] = pygame.transform.rotate(pygame.image.load("gfx/birdN.png").convert_alpha(),225)
        sprites["obst"] = pygame.transform.rotate(pygame.image.load("gfx/obst.png").convert_alpha(),0)
        sprites["screen"] = pygame.transform.scale_by(pygame.image.load("gfx/screen.jpg"),1).convert_alpha()
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
        if self.tracker is not None:
            self.tracker.quit()

g = Game()
g.run()