from .utils import Scene, SceneManager, Button
from .player import Player
from .npc import NPC
from .block import Block
import pygame, time

class GameScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict, level: str) -> None:

        super().__init__(manager, screen, tracker, sprites)

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
        self.player = Player(100,200,self.sprites["ship"])
        self.npcs   = [NPC(self.sprites["ship"]) for _ in range(10)]
        self.blocks = [Block((i+1)*50,(i+1)*20, 10, None) for i in range(10)]

    def update(self) -> None:

        dt = self.update_time()
        self.player.update(dt)
        for npc in self.npcs:
            npc.set_direction(self.player)
            npc.update(dt)
        for block in self.blocks:
            block.update(dt)
        self.score_cell.text = f"SPEED: {int(10*self.player.speed/self.player.spe_c)}"
        self.score_cell.update(dt)

    def render(self) -> None:
        self.screen.fill("black")
        for block in self.blocks: block.render(self.screen)
        for npc in self.npcs: npc.render(self.screen)
        self.player.render(self.screen)
        self.score_cell.render(self.screen)
        pygame.display.update()

    def poll_events(self) -> None:

        if self.tracker is not None:
            self.tracker.track()

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