from utils import Scene, SceneManager
from player import Player
from npc import NPC
import pygame, time

class GameScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict) -> None:

        super().__init__(manager, screen, sprites)

        self.player = Player(100,200,self.sprites["ship"])
        self.npcs   = [NPC(self.sprites["ship"]) for _ in range(10)]

        # User input system
        self.keybinds = {pygame.K_w: "N",
                         pygame.K_d: "E",
                         pygame.K_s: "S",
                         pygame.K_a: "W"}
        self.keystack = []
        self.current_key = None

    def update(self) -> None:

        dt = self.update_time()
        self.player.update(dt)
        for npc in self.npcs: npc.update(dt)

    def render(self) -> None:
        self.screen.fill("black")
        self.player.render(self.screen)
        for npc in self.npcs: npc.render(self.screen)
        pygame.display.update()

    def poll_events(self) -> None:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.manager.quit_game()
        
            if event.type == pygame.KEYDOWN and event.key in self.keybinds: self.keystack.append(event.key)
            if event.type == pygame.KEYUP   and event.key in self.keybinds: self.keystack.remove(event.key)

            if len(self.keystack):
                if self.current_key != self.keystack[-1]:
                    self.current_key = self.keystack[-1]

                    self.player.set_direction(self.keybinds[self.current_key])
                    for npc in self.npcs:
                        npc.set_direction(self.keybinds[self.current_key])
                        npc.moving = True
                    self.player.moving = True
            else:
                self.current_key   = None
                for npc in self.npcs: npc.moving = False
                #self.player.moving = False