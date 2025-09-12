from flock import glob, args, opts
from flock import SceneManager, MenuScene, GameScene, OptiScene, Tracker, ObstScene, CredScene
import pygame, time
import pygame.transform as pt
from pygame.image import load as pil

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
        scenes = {"opti": OptiScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "menu": MenuScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "obst": ObstScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "cred": CredScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "game": GameScene(self.scene_manager, self.screen, self.tracker, self.sprites)
                  }
        starting_scene = "menu"
        self.scene_manager.initialize(scenes, starting_scene)
        if starting_scene == "game": scenes["game"].build_level()
        self.scene_manager.scenes["opti"].change_settings()

    def load_image(self, image, scale, rot, flip_x=False, flip_y=False):
        image = pil(image).convert_alpha()
        image = pt.flip(image, flip_x=flip_x, flip_y=flip_y)
        image = pt.rotate(image, rot)
        image = pt.scale_by(image, scale)
        return image

    def load_sprites(self) -> dict: 
        """ Load sprite textures into pygame as surfaces and returns a dictionary of names to surfaces. """
        
        sprites = {}

        # UCCELLI
        sprites["0led"] = self.load_image("gfx/scen0/birdL.png", 1, 235)
        sprites["0npc"] = self.load_image("gfx/scen0/birdN.png", 1, 235)
        sprites["0scr"] = self.load_image("gfx/scen0/sky.jpg", 1, 0)
        sprites["0obs"] = self.load_image("gfx/scen0/flock_obst.png",   0.7, 0)
        sprites["0tar"] = self.load_image("gfx/scen0/flock_target.png", 0.7, 0)

        # PESCI
        sprites["1led"] = self.load_image("gfx/scen1/nemo.png", 1.3, 0, flip_x=True, flip_y=False)
        sprites["1npc"] = self.load_image("gfx/scen1/dory.png", 1.3, 0) 
        sprites["1scr"] = self.load_image("gfx/scen1/ocean.jpg", 1, 0)
        sprites["1obs"] = self.load_image("gfx/scen1/fish_obst_2.png", 0.4, 0)
        sprites["1tar"] = self.load_image("gfx/scen1/fish_target.png", 0.5, 0)

        # ABSTRACT
        sprites["2led_1"] = self.load_image("gfx/scen2/f1.png", 0.25, 90)
        sprites["2led_2"] = self.load_image("gfx/scen2/f2.png", 0.25, 90)
        sprites["2led_3"] = self.load_image("gfx/scen2/f3.png", 0.25, 90)
        sprites["2led_4"] = self.load_image("gfx/scen2/f2.png", 0.25, 90)
        sprites["2npc_1"] = self.load_image("gfx/scen2/m1.png", 0.20, 90)
        sprites["2npc_2"] = self.load_image("gfx/scen2/m2.png", 0.20, 90)
        sprites["2npc_3"] = self.load_image("gfx/scen2/m3.png", 0.20, 90)
        sprites["2npc_4"] = self.load_image("gfx/scen2/m2.png", 0.20, 90)
        sprites["2scr"]   = self.load_image("gfx/scen2/abstract_bckg.png", 1.4, 0)
        sprites["2obs"]   = self.load_image("gfx/scen2/abstract_obst.png", 0.4, 0)
        sprites["2tar"]   = self.load_image("gfx/scen2/abstract_target.png", 0.1, 0)

        # ABSTRACT
        sprites["3led"] = self.load_image("gfx/scen3/orange_dot.png", 0.20, 0)
        sprites["3npc"] = self.load_image("gfx/scen3/black_dot.png", 0.16, 0)
        sprites["3scr"] = self.load_image("gfx/scen3/abstract_bckg.png", 1.4, 0)
        sprites["3obs"] = self.load_image("gfx/scen3/abstract_obst.png", 0.4, 0)
        sprites["3tar"] = self.load_image("gfx/scen3/abstract_target.png", 0.1, 0)

        # Easter Egg 1
        sprites["4led"] = self.load_image("gfx/ee1/miki_langelo.png", 6, -90)
        sprites["4npc"] = self.load_image("gfx/ee1/giogio.png", 1, -90)
        sprites["4scr"] = self.load_image("gfx/ee1/grass.jpg", 1, 0)
        sprites["4obs"] = self.load_image("gfx/ee1/obst.png", 0.3, 0)
        sprites["4tar"] = self.load_image("gfx/ee1/zirli_ovini_target.png", 0.0042, 0)

        # Easter Egg 2
        sprites["5led"] = self.load_image("gfx/ee2/stetuned.png",  2., -90)
        sprites["5npc"] = self.load_image("gfx/ee2/instarega.png", 2., -90)
        sprites["5scr"] = self.load_image("gfx/ee2/ocean.jpg", 1, 0)
        sprites["5obs"] = self.load_image("gfx/ee2/flock_obst.png", 0.7, 0)
        sprites["5tar"] = self.load_image("gfx/ee2/mox_target.png", 0.6, 0)

        # GENERAL
        sprites["compass"] = self.load_image("gfx/misc/compass.png", 1, 0)
        sprites["needle"]  = self.load_image("gfx/misc/needle.png", 1, 270)
        sprites["logo"]    = self.load_image("gfx/misc/logo.png", 0.5, 0)

        sprites["diff0"] = self.load_image("gfx/icons/diff_0.png", 1, 0)
        sprites["diff1"] = self.load_image("gfx/icons/diff_1.png", 1, 0)
        sprites["diff2"] = self.load_image("gfx/icons/diff_2.png", 1, 0)

        sprites["scen0"] = self.load_image("gfx/icons/scen_0.png", 1, 0)
        sprites["scen1"] = self.load_image("gfx/icons/scen_1.png", 1, 0)
        sprites["scen2"] = self.load_image("gfx/icons/scen_2.png", 1, 0)

        sprites["obst0"] = self.load_image("gfx/icons/obst_0.png", 1, 0)
        sprites["obst1"] = self.load_image("gfx/icons/obst_1.png", 1, 0)
        sprites["obst2"] = self.load_image("gfx/icons/obst_1.png", 1, 0)

        sprites["mode0"] = self.load_image("gfx/icons/mode_0.png", 1, 0)
        sprites["mode1"] = self.load_image("gfx/icons/mode_1.png", 1, 0)
        sprites["mode2"] = self.load_image("gfx/icons/mode_1.png", 1, 0)

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