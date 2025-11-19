import warnings, sys, os
warnings.filterwarnings("ignore", category=RuntimeWarning)
original_stdout, original_stderr = sys.stdout, sys.stderr
sys.stdout, sys.stderr = open(os.devnull, 'w'), open(os.devnull, 'w')
import pygame
sys.stdout, sys.stderr = original_stdout, original_stderr

import time
import pygame.transform as pt
from pygame.image import load as pil

from flock import glob
from flock import SceneManager, MenuScene, GameScene, OptiScene, Tracker, ObstScene, CredScene

class Game:

    def __init__(self) -> None:
        """ Initialize global game variables """

        self.running = True
        self.screen  = pygame.display.set_mode((int(glob.SW*glob.SF), int(glob.SH*glob.SF)))
        self.tracker = Tracker() if glob.TRACKER_FLAG else None
        self.sprites = self._load_sprites()
        self._load_scenes(starting_scene="menu")

    def _load_scenes(self, starting_scene="menu") -> None:

        self.scene_manager = SceneManager()
        scenes = {"opti": OptiScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "menu": MenuScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "obst": ObstScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "cred": CredScene(self.scene_manager, self.screen, self.tracker, self.sprites),
                  "game": GameScene(self.scene_manager, self.screen, self.tracker, self.sprites)
                  }

        self.scene_manager.initialize(scenes, starting_scene)
        if starting_scene == "game": scenes["game"].build_level()
        self.scene_manager.scenes["opti"].change_settings()

    def _load_sprites(self) -> dict: 
        """ Load sprite textures into pygame as surfaces and returns a dictionary of names to surfaces. """
        
        sprites = {}
        
        def load_image(image, scale, rot, flip_x=False, flip_y=False):
            image = pil(image).convert_alpha()
            image = pt.flip(image, flip_x=flip_x, flip_y=flip_y)
            image = pt.rotate(image, rot)
            image = pt.scale_by(image, scale)
            return image

        # UCCELLI
        sprites["0led"] = load_image("gfx/scen0/birdL.png", 1, 235)
        sprites["0npc"] = load_image("gfx/scen0/birdN.png", 1, 235)
        sprites["0scr"] = load_image("gfx/scen0/sky.jpg", 1, 0)
        sprites["0obs"] = load_image("gfx/scen0/flock_obst.png",   0.7, 0)
        sprites["0tar"] = load_image("gfx/scen0/flock_target.png", 0.7, 0)

        # PESCI
        sprites["1led"] = load_image("gfx/scen1/nemo.png", 1.3, 0, flip_x=True, flip_y=False)
        sprites["1npc"] = load_image("gfx/scen1/dory.png", 1.3, 0) 
        sprites["1scr"] = load_image("gfx/scen1/ocean_2.jpeg", 0.82, 0)
        sprites["1obs"] = load_image("gfx/scen1/fish_obst_2.png", 0.4, 0)
        sprites["1tar"] = load_image("gfx/scen1/fish_target.png", 0.5, 0)

        # HUMANS
        sprites["2led_1"] = load_image("gfx/scen2/f1.png", 0.25, 90)
        sprites["2led_2"] = load_image("gfx/scen2/f2.png", 0.25, 90)
        sprites["2led_3"] = load_image("gfx/scen2/f3.png", 0.25, 90)
        sprites["2led_4"] = load_image("gfx/scen2/f2.png", 0.25, 90)
        sprites["2npc_1"] = load_image("gfx/scen2/m1.png", 0.20, 90)
        sprites["2npc_2"] = load_image("gfx/scen2/m2.png", 0.20, 90)
        sprites["2npc_3"] = load_image("gfx/scen2/m3.png", 0.20, 90)
        sprites["2npc_4"] = load_image("gfx/scen2/m2.png", 0.20, 90)
        sprites["2scr"]   = load_image("gfx/scen2/runner_bckg_3.jpeg", 0.8, 0, flip_x=True) # 0.8 per 2bis 
        sprites["2obs"]   = load_image("gfx/scen2/runner_obst_3.png", 0.6, 0) # 0.3 per conetto, 0.8 per buca, 0.6 per fuoco 
        sprites["2tar"]   = load_image("gfx/scen2/runner_target.png", 0.35, 0)

        # ABSTRACT
        sprites["3led"] = load_image("gfx/scen3/orange_dot.png", 0.20, 0)
        sprites["3npc"] = load_image("gfx/scen3/black_dot.png", 0.16, 0)
        sprites["3scr"] = load_image("gfx/scen3/abstract_bckg.png", 1.4, 0)
        sprites["3obs"] = load_image("gfx/scen3/abstract_obst.png", 0.4, 0)
        sprites["3tar"] = load_image("gfx/scen3/abstract_target.png", 0.1, 0)

        # Easter Egg 1
        sprites["4led"] = load_image("gfx/ee1/miki_langelo.png", 6, -90)
        sprites["4npc"] = load_image("gfx/ee1/giogio.png", 1, -90)
        sprites["4scr"] = load_image("gfx/ee1/grass.jpg", 1, 0)
        sprites["4obs"] = load_image("gfx/ee1/obst.png", 0.3, 0)
        sprites["4tar"] = load_image("gfx/ee1/zirli_ovini_target.png", 0.0042, 0)

        # Easter Egg 2
        sprites["5led"] = load_image("gfx/ee2/stetuned.png",  2., -90)
        sprites["5npc"] = load_image("gfx/ee2/instarega.png", 2., -90)
        sprites["5scr"] = load_image("gfx/ee2/ocean.jpg", 1, 0)
        sprites["5obs"] = load_image("gfx/ee2/flock_obst.png", 0.7, 0)
        sprites["5tar"] = load_image("gfx/ee2/mox_target.png", 0.6, 0)

        # GENERAL
        sprites["compass"] = load_image("gfx/misc/compass.png", 1, 0)
        sprites["needle"]  = load_image("gfx/misc/needle.png", 1, 270)
        sprites["logo"]    = load_image("gfx/misc/logo.png", 0.5, 0)
        sprites["logo_dmat"] = load_image("gfx/misc/logo_dmat.png", 0.5, 0)

        sprites["diff0"] = load_image("gfx/icons/velo_0.png", 1, 0)
        sprites["diff1"] = load_image("gfx/icons/velo_1.png", 1, 0)
        sprites["diff2"] = load_image("gfx/icons/velo_2.png", 1, 0)

        sprites["scen0"] = load_image("gfx/icons/scen_0.png", 1, 0)
        sprites["scen1"] = load_image("gfx/icons/scen_1.png", 1, 0)
        sprites["scen2"] = load_image("gfx/icons/scen_2bis.png", 0.5, 0)

        sprites["obst0"] = load_image("gfx/icons/obst_0.png", 1, 0)
        sprites["obst1"] = load_image("gfx/icons/obst_1.png", 1, 0)
        sprites["obst2"] = load_image("gfx/icons/obst_2.png", 0.5, 0)

        sprites["mode0"] = load_image("gfx/icons/mode_0.png", 1, 0)
        sprites["mode1"] = load_image("gfx/icons/mode_1.png", 1, 0)
        sprites["mode2"] = load_image("gfx/icons/mode_2.png", 2, 0)

        sprites["posNW"] = load_image("gfx/icons/posNW.png", 1, 0)
        sprites["posNC"] = load_image("gfx/icons/posNC.png", 1, 0)
        sprites["posNE"] = load_image("gfx/icons/posNE.png", 1, 0)
        sprites["posSW"] = load_image("gfx/icons/posSW.png", 1, 0)
        sprites["posSC"] = load_image("gfx/icons/posSC.png", 1, 0)
        sprites["posSE"] = load_image("gfx/icons/posSE.png", 1, 0)
        sprites["emptySW"] = load_image("gfx/icons/emptySW.png", 1, 0)

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

pygame.init()
g = Game()
g.run()