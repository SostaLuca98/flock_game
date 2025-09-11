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
        sprites["0led"] = self.load_image("gfx/birdL.png", 1, 235)
        sprites["0npc"] = self.load_image("gfx/birdN.png", 1, 235)
        sprites["0scr"] = self.load_image("gfx/sky.jpg", 1, 0)
        sprites["0obs"] = self.load_image("gfx/flock_obst.png",   0.7, 0)
        sprites["0tar"] = self.load_image("gfx/flock_target.png", 0.7, 0)

        # PESCI
        sprites["1led"] = self.load_image("gfx/nemo.png", 1.3, 0, flip_x=True, flip_y=False)
        sprites["1npc"] = self.load_image("gfx/dory.png", 1.3, 0) 
        sprites["1scr"] = self.load_image("gfx/ocean.jpg", 1, 0)
        sprites["1obs"] = self.load_image("gfx/fish_obst_2.png", 0.4, 0)
        sprites["1tar"] = self.load_image("gfx/fish_target.png", 0.5, 0)

        # ABSTRACT
        sprites["2led_1"] = self.load_image("gfx/f1.png", 0.25, 90)
        sprites["2led_2"] = self.load_image("gfx/f2.png", 0.25, 90)
        sprites["2led_3"] = self.load_image("gfx/f3.png", 0.25, 90)
        sprites["2led_4"] = self.load_image("gfx/f2.png", 0.25, 90)
        sprites["2npc_1"] = self.load_image("gfx/m1.png", 0.20, 90)
        sprites["2npc_2"] = self.load_image("gfx/m2.png", 0.20, 90)
        sprites["2npc_3"] = self.load_image("gfx/m3.png", 0.20, 90)
        sprites["2npc_4"] = self.load_image("gfx/m2.png", 0.20, 90)
        sprites["2scr"]   = self.load_image("gfx/abstract_bckg.png", 1.4, 0)
        sprites["2obs"]   = self.load_image("gfx/abstract_obst.png", 0.4, 0)
        sprites["2tar"]   = self.load_image("gfx/abstract_target.png", 0.1, 0)

        # ABSTRACT
        sprites["3led"] = self.load_image("gfx/orange_dot.png", 0.20, 0)
        sprites["3npc"] = self.load_image("gfx/black_dot.png", 0.16, 0)
        sprites["3scr"] = self.load_image("gfx/abstract_bckg.png", 1.4, 0)
        sprites["3obs"] = self.load_image("gfx/abstract_obst.png", 0.4, 0)
        sprites["3tar"] = self.load_image("gfx/abstract_target.png", 0.1, 0)

        # Easter Egg 1
        sprites["4led"] = pt.rotate(pt.scale_by(pil("gfx_2/miki_langelo.png").convert_alpha(),6), -90)
        sprites["4npc"] = pt.rotate(pt.scale_by(pil("gfx_2/giogio.png").convert_alpha(),1), -90)
        sprites["4scr"] = pt.scale_by(pil("gfx/grass_3.jpg"),1).convert_alpha()
        sprites["4obs"] = pt.rotate(pil("gfx/obst.png").convert_alpha(),0)
        sprites["4tar"] = pt.scale_by(pil("gfx/zirli_ovini_target.png").convert_alpha(), 0.0042)

        # Easter Egg 2
        sprites["5led"] = pt.rotate(pt.scale_by(pil( "gfx_2/stetuned.png").convert_alpha(),2.),-90)
        sprites["5npc"] = pt.rotate(pt.scale_by(pil("gfx_2/instarega.png").convert_alpha(),2.),-90)
        sprites["5scr"] = pt.scale_by(pil("gfx/ocean.jpg"),1).convert_alpha()
        sprites["5obs"] = self.load_image("gfx/flock_obst.png",   0.7, 0)
        sprites["5tar"] = self.load_image("gfx_2/mox_target.png", 0.6, 0)#pt.scale_by(pil("gfx_2/mox_target.png").convert_alpha(), 2*0.0042)

        # GENERAL
        sprites["compass"] = pt.rotate(pil("gfx/compass.png").convert_alpha(),0)
        sprites["needle"] = pt.rotate(pil("gfx/needle.png").convert_alpha(),270)
        sprites["logo"] = self.load_image("gfx/logo.png", 0.5, 0)

        sprites["diff0"] = pt.scale_by(pil("gfx/diff_0.png"),1).convert_alpha()
        sprites["diff1"] = pt.scale_by(pil("gfx/diff_1.png"),1).convert_alpha()
        sprites["diff2"] = pt.scale_by(pil("gfx/diff_2.png"),1).convert_alpha()

        sprites["scen0"] = pt.scale_by(pil("gfx/scen_0.png"),1).convert_alpha()
        sprites["scen1"] = pt.scale_by(pil("gfx/scen_1.png"),1).convert_alpha()
        sprites["scen2"] = pt.scale_by(pil("gfx/scen_2.png"),1).convert_alpha()

        sprites["obst0"] = pt.scale_by(pil("gfx/obst_0.png"), 1).convert_alpha()
        sprites["obst1"] = pt.scale_by(pil("gfx/obst_1.png"), 1).convert_alpha()
        sprites["obst2"] = pt.scale_by(pil("gfx/obst_1.png"), 1).convert_alpha()

        sprites["mode0"] = pt.scale_by(pil("gfx/mode_0.png"),1).convert_alpha()
        sprites["mode1"] = pt.scale_by(pil("gfx/mode_1.png"),1).convert_alpha()
        sprites["mode2"] = pt.scale_by(pil("gfx/mode_1.png"),1).convert_alpha()

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