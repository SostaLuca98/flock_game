from .utils import Scene, SceneManager, Button
from .player import Player
from .npc import NPC
from .block import Block
from .engine import Engine
import pygame, numpy
from .config import args

class GameScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict, level: str) -> None:

        super().__init__(manager, screen, tracker, sprites)

        self.args = args
        self.keybinds_dir = {pygame.K_w: "N",
                             pygame.K_d: "E",
                             pygame.K_s: "S",
                             pygame.K_a: "W"}
        self.keystack_dir = []
        self.curr_key_dir = None
        
        self.keybinds_spe = {pygame.K_UP: "U", pygame.K_DOWN: "D", pygame.K_RIGHT : "R"}
        self.keystack_spe = []
        self.curr_key_spe = None

        self.score_cell = Button(1100, 680, "")

        self.level = level
        self.build_level()

    def build_level(self):
        self.blocks = [Block(self.args, 500, 200, 50, self.sprites["obst"])]
        self.npcs   = [NPC(self.args,self.sprites["birdN"]) for _ in range(self.args.n)]
        self.player = Player(self.args, 100,200,self.sprites["birdL"])
        self.engine = Engine(self.args, self.player, self.npcs, self.blocks)

    def update(self) -> None:

        dt = self.update_time()
        self.engine.update(dt)

        #self.score_cell.text = f"SPEED: {int(10*self.player.speed/self.player.spe_c)}"
        self.score_cell.text = f"ANGLE: {-int(self.player.tar_angle*360/2/numpy.pi)}"
        self.score_cell.update(dt)

    def render(self) -> None:
        self.screen.fill("black")
        self.screen.blit(pygame.transform.scale_by(self.sprites["screen"], args.SF),(0,0))
        for block in self.blocks: block.render(self.screen)
        for npc in self.npcs: npc.render(self.screen)
        angle = -self.player.tar_angle*360/(2*numpy.pi)
        compass = pygame.transform.scale_by(self.sprites["compass"], 0.3*args.SF)
        needle  = pygame.transform.rotate(pygame.transform.scale_by(self.sprites["needle"], 0.3*args.SF),angle)
        self.screen.blit(compass,(1200*args.SF-compass.get_size()[0]/2,100*args.SF-compass.get_size()[1]/2))
        self.screen.blit(needle, (1200*args.SF- needle.get_size()[0]/2,100*args.SF- needle.get_size()[1]/2))
        self.player.render(self.screen)
        self.score_cell.render(self.screen)
        pygame.display.update()

    def poll_events(self) -> None:

        if self.tracker is not None:
            angle = self.tracker.track()
            if angle is not None:
                self.player.tar_angle = angle/360*2*numpy.pi

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
                    if self.keybinds_spe[self.curr_key_spe] != "R":
                        self.player.set_speed(self.keybinds_spe[self.curr_key_spe])
                    else: 
                        self.player.speed = self.player.spe_c
                        self.player.set_speed("0")
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
