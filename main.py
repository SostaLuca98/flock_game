from flock import glob, args, opts
from flock import SceneManager, MenuScene, GameScene, OptiScene, Tracker, ObstScene
import pygame, time

import warnings
warnings.simplefilter('error', RuntimeWarning)

class Game:

    def __init__(self) -> None:
        """ Initialize global game variables """

        pygame.init()
        self.running = True
        self.screen  = pygame.display.set_mode((int(glob.SW*glob.SF), int(glob.SH*glob.SF)))
        self.tracker = Tracker() if glob.TRACKER_FLAG else None
        self.sprites = self.load_sprites()
        self.load_scenes()

    def load_scenes(self) -> None:
        self.scene_manager = SceneManager()
        scenes = {"game": GameScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "menu": MenuScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "opti": OptiScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "obst": ObstScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  }
        self.scene_manager.initialize(scenes, "menu") # DI BASE ANDREBBE MENU
        self.scene_manager.scenes["opti"].change_settings()


    def load_sprites(self) -> dict: 
        """ Load sprite textures into pygame as surfaces and returns a dictionary of names to surfaces. """
        
        sprites = {}

        # UCCELLI
        sprites["0led"] = pygame.transform.rotate(pygame.image.load("gfx/birdL.png").convert_alpha(), 225)
        sprites["0npc"] = pygame.transform.rotate(pygame.image.load("gfx/birdN.png").convert_alpha(), 225)
        sprites["0scr"] = pygame.transform.scale_by(pygame.image.load("gfx/sky.jpg"),1).convert_alpha()
        sprites["0obs"] = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("gfx/flock_obst.png"), 2).convert_alpha(),0)
        sprites["0tar"] = pygame.transform.scale_by(pygame.image.load("gfx/flock_target.png").convert_alpha(), 3)

        # PESCI
        sprites["1led"] = pygame.transform.flip(pygame.image.load("gfx/nemo.png").convert_alpha(),flip_x=True, flip_y=False)
        sprites["1npc"] = pygame.transform.rotate(pygame.image.load("gfx/dory.png").convert_alpha(),0)
        sprites["1scr"] = pygame.transform.scale_by(pygame.image.load("gfx/ocean.jpg"),1).convert_alpha()
        sprites["1obs"] = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("gfx/fish_obst_2.png").convert_alpha(), 1.5), 0)
        sprites["1tar"] = pygame.transform.scale_by(pygame.image.load("gfx/fish_target.png").convert_alpha(), 2)

        # PECORE
        sprites["2led"] = pygame.transform.scale_by(pygame.image.load("gfx/doggo.png").convert_alpha(),1.8)
        sprites["2npc"] = pygame.transform.flip(pygame.transform.scale_by(pygame.image.load("gfx/dolly.png").convert_alpha(),1.8), flip_x=True, flip_y=False)
        #sprites["2npc"] = pygame.transform.scale_by(pygame.image.load("gfx/zirli_ovini_target.png").convert_alpha(), 1.8)
        sprites["2scr"] = pygame.transform.scale_by(pygame.image.load("gfx/grass_3.jpg"),1).convert_alpha()
        sprites["2obs"] = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("gfx/dolly_obst.png").convert_alpha(), 2),0)
        sprites["2tar"] = pygame.transform.scale_by(pygame.image.load("gfx/dolly_target.png").convert_alpha(), 3)

        # Easter Egg 1
        sprites["3led"] = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("gfx_2/miki_langelo.png").convert_alpha(),6), -90)
        sprites["3npc"] = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("gfx_2/giogio.png").convert_alpha(),1), -90)
        #sprites["2npc"] = pygame.transform.scale_by(pygame.image.load("gfx/zirli_ovini_target.png").convert_alpha(), 1.8)
        sprites["3scr"] = pygame.transform.scale_by(pygame.image.load("gfx/grass_3.jpg"),1).convert_alpha()
        sprites["3obs"] = pygame.transform.rotate(pygame.image.load("gfx/obst.png").convert_alpha(),0)
        sprites["3tar"] = pygame.transform.scale_by(pygame.image.load("gfx/zirli_ovini_target.png").convert_alpha(), 1)

        # Easter Egg 2
        sprites["4led"] = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load( "gfx_2/stetuned.png").convert_alpha(),2.5),-90)
        sprites["4npc"] = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("gfx_2/instarega.png").convert_alpha(),2.5),-90)
        #sprites["2npc"] = pygame.transform.scale_by(pygame.image.load("gfx/zirli_ovini_target.png").convert_alpha(), 1.8)
        sprites["4scr"] = pygame.transform.scale_by(pygame.image.load("gfx/ocean.jpg"),1).convert_alpha()
        sprites["4obs"] = pygame.transform.rotate(pygame.image.load("gfx/obst.png").convert_alpha(),0)
        sprites["4tar"] = pygame.transform.scale_by(pygame.image.load("gfx_2/mox_target.png").convert_alpha(), 1)

        # GENERAL
        sprites["compass"] = pygame.transform.rotate(pygame.image.load("gfx/compass.png").convert_alpha(),0)
        sprites["needle"] = pygame.transform.rotate(pygame.image.load("gfx/needle.png").convert_alpha(),270)

        sprites["diff0"] = pygame.transform.scale_by(pygame.image.load("gfx/diff_0.png"),1).convert_alpha()
        sprites["diff1"] = pygame.transform.scale_by(pygame.image.load("gfx/diff_1.png"),1).convert_alpha()
        sprites["diff2"] = pygame.transform.scale_by(pygame.image.load("gfx/diff_2.png"),1).convert_alpha()

        sprites["scen0"] = pygame.transform.scale_by(pygame.image.load("gfx/scen_0.png"),1).convert_alpha()
        sprites["scen1"] = pygame.transform.scale_by(pygame.image.load("gfx/scen_1.png"),1).convert_alpha()
        sprites["scen2"] = pygame.transform.scale_by(pygame.image.load("gfx/scen_2.png"),1).convert_alpha()

        sprites["obst0"] = pygame.transform.scale_by(pygame.image.load("gfx/obst_0.png"), 1).convert_alpha()
        sprites["obst1"] = pygame.transform.scale_by(pygame.image.load("gfx/obst_1.png"), 1).convert_alpha()

        sprites["mode0"] = pygame.transform.scale_by(pygame.image.load("gfx/mode_0.png"),1).convert_alpha()
        sprites["mode1"] = pygame.transform.scale_by(pygame.image.load("gfx/mode_1.png"),1).convert_alpha()

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