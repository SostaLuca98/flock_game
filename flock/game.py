from .utils import Scene, SceneManager, Button
from .player import Player
from .npc import NPC
from .block import Block
from .engine import Engine
import pygame, time, numpy
from dataclasses import dataclass

class GameScene(Scene):

    @dataclass
    class Params:
        n = 200 # Numero di elementi dello stormo
        w = 1000  # Numero di leader
        T = 20 # Numero di istanti temporali simulati
        ps = 10 # plot ogni tot istanti (utile in sviluppo)
        x_max = 1280 # Lunghezza del dominio
        y_max = 720  # Altezza del dominio
        x0_max = 300
        y0_max = 150
        theta0_avg = 0
        theta0_var = numpy.pi/6
        v = 1  # Lunghezza di 1 passo temporale
        r = 50 # Raggio legame di vicinanza

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict, level: str) -> None:

        super().__init__(manager, screen, tracker, sprites)

        self.args = self.Params()
        self.keybinds_dir = {pygame.K_w: "N",
                             pygame.K_d: "E",
                             pygame.K_s: "S",
                             pygame.K_a: "W"}
        self.keystack_dir = []
        self.curr_key_dir = None
        
        self.keybinds_spe = {pygame.K_UP: "U", pygame.K_DOWN: "D"}
        self.keystack_spe = []
        self.curr_key_spe = None

        self.score_cell = Button(1100, 680, "")

        self.build_level(level)

    def build_level(self, level):
        self.player = Player(100,200,self.sprites["capo"])
        self.npcs   = [NPC(self.sprites["bird"]) for _ in range(self.args.n)]
        self.blocks = [Block((i+1)*50,(i+1)*20, 10, None) for i in range(10)]
        self.engine = Engine(self.args, self.player, self.npcs, self.blocks)

    def update(self) -> None:

        dt = self.update_time()
        self.engine.update(dt)

        for block in self.blocks:
            block.update(dt)

        #self.score_cell.text = f"SPEED: {int(10*self.player.speed/self.player.spe_c)}"
        self.score_cell.text = f"ANGLE: {-int(self.player.tar_angle*360/2/numpy.pi)}"
        self.score_cell.update(dt)

    def render(self) -> None:
        self.screen.fill((13//1.2, 128//1.2, 96//1.2))
        for block in self.blocks: block.render(self.screen)
        for npc in self.npcs: npc.render(self.screen)
        self.player.render(self.screen)
        self.score_cell.render(self.screen)
        pygame.display.update()

    def poll_events(self) -> None:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.manager.quit_game()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.quit_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.manager.set_scene("menu")
        
            if event.type == pygame.KEYDOWN: 
                if event.key in self.keybinds_dir: self.keystack_dir.append(event.key)
                if event.key in self.keybinds_spe: self.keystack_spe.append(event.key)
            if event.type == pygame.KEYUP: 
                if event.key in self.keybinds_dir: self.keystack_dir.remove(event.key)
                if event.key in self.keybinds_spe: self.keystack_spe.remove(event.key)

            if len(self.keystack_spe):
                if  self.curr_key_spe != self.keystack_spe[-1]:
                    self.curr_key_spe  = self.keystack_spe[-1]

                    self.player.set_speed(self.keybinds_spe[self.curr_key_spe])
            else:
                self.curr_key_spe = None
                self.player.set_speed("0")

            if len(self.keystack_dir):
                if  self.curr_key_dir != self.keystack_dir[-1]:
                    self.curr_key_dir  = self.keystack_dir[-1]

                    self.player.set_direction(self.keybinds_dir[self.curr_key_dir])
                    self.player.moving = True
            else: 
                self.curr_key_dir = None

        if self.tracker is not None:
            angle = self.tracker.track()
            if angle is not None:
                self.player.tar_angle = angle/360*2*numpy.pi