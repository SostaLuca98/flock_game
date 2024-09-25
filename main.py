from flock import args, options
from flock import SceneManager, MenuScene, GameScene, OptiScene, Tracker
import pygame, time

class Game:

    def __init__(self) -> None:
        """ Initialize global game variables """

        pygame.init()
        self.running = True
        self.screen  = pygame.display.set_mode((int(args.SW*args.SF), int(args.SH*args.SF)))
        self.tracker = Tracker() if args.TRACKER_FLAG else None
        self.sprites = self.load_sprites()
        self.load_scenes()

    def load_scenes(self) -> None:
        self.scene_manager = SceneManager()
        scenes = {"game": GameScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "menu": MenuScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "opti": OptiScene(self.scene_manager, self.screen, self.tracker, self.sprites)}
        self.scene_manager.initialize(scenes, "menu") # DI BASE ANDREBBE MENU


    def load_sprites(self) -> dict: 
        """ Load sprite textures into pygame as surfaces and returns a dictionary of names to surfaces. """
        
        sprites = {}

        # UCCELLI
        sprites["0led"] = pygame.transform.rotate(pygame.image.load("gfx/birdL.png").convert_alpha(), 225)
        sprites["0npc"] = pygame.transform.rotate(pygame.image.load("gfx/birdN.png").convert_alpha(), 225)
        sprites["0scr"] = pygame.transform.scale_by(pygame.image.load("gfx/screen.jpg"),1).convert_alpha()
        sprites["0obs"] = pygame.transform.rotate(pygame.image.load("gfx/obst.png").convert_alpha(),0)

        # PESCI
        sprites["1led"] = pygame.transform.flip(pygame.image.load("gfx/nemo.png").convert_alpha(),flip_x=True, flip_y=False)
        sprites["1npc"] = pygame.transform.rotate(pygame.image.load("gfx/dory.png").convert_alpha(),0)
        sprites["1scr"] = pygame.transform.scale_by(pygame.image.load("gfx/ocean.jpg"),1).convert_alpha()
        sprites["1obs"] = pygame.transform.rotate(pygame.image.load("gfx/obst.png").convert_alpha(),0)

        # PECORE
        sprites["2led"] = pygame.transform.flip(pygame.image.load("gfx/nemo.png").convert_alpha(),flip_x=True, flip_y=False)
        sprites["2npc"] = pygame.transform.rotate(pygame.image.load("gfx/dory.png").convert_alpha(),0)
        sprites["2scr"] = pygame.transform.scale_by(pygame.image.load("gfx/ocean.jpg"),1).convert_alpha()
        sprites["2obs"] = pygame.transform.rotate(pygame.image.load("gfx/obst.png").convert_alpha(),0)

        # GENERAL
        sprites["compass"] = pygame.transform.rotate(pygame.image.load("gfx/compass.png").convert_alpha(),0)
        sprites["needle"] = pygame.transform.rotate(pygame.image.load("gfx/needle.png").convert_alpha(),270)

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