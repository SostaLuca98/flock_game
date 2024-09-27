from .config import glob, args, opts
from .utils import Scene, SceneManager, Button
from .player import Player
from .npc import NPC
from .block import Block
from .engine import Engine
import pygame, numpy, time

class GameScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:

        super().__init__(manager, screen, tracker, sprites)

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
        self.time_cell  = Button(200, 680, "")
        self.build_flag = False

        self.scenario  = opts.scen
        self.target = Block(args, 100, 500, 75, self.sprites[f"{self.scenario}tar"])

    def build_level(self):

        self.scenario  = opts.scen
        self.target.sprite = self.sprites[f"{self.scenario}tar"]
        self.manager.scenes["opti"].change_settings()

        if opts.obst == 0:
            self.blocks = [Block(args, 500, 200, 50, self.sprites[f"{self.scenario}obs"])]
        elif opts.obst == 1:
            reader = self.manager.scenes['obst'].reader
            self.blocks = [Block(args,
                                 reader.x_centers[i]+0.5,
                                 reader.y_centers[i]+0.5,
                                 reader.radii[i],
                                 self.sprites[f"{self.scenario}obs"]) for i,_ in enumerate(reader.x_centers)]

        self.npcs   = [NPC(args, self.sprites[f"{self.scenario}npc"]) for _ in range(args.n)]
        self.player = Player(args, 100,200,self.sprites[f"{self.scenario}led"])
        self.engine = Engine(args, self.manager.scenes["game"])

        self.score = 0
        self.t0 = time.time()
        self.time = args.t_max

    def update(self) -> None:

        if not self.build_flag:
            self.build_flag = True
            self.build_level()

        dt = self.update_time()
        self.engine.update(dt)

        if opts.mode == 1:
            self.time = int(args.t_max - (time.time()-self.t0))
            self.score_cell.text = f"SCORE: {self.score}"
            self.score_cell.update(dt)
            self.time_cell.text = f"TIME: {self.time}"
            self.time_cell.update(dt)

    def render(self) -> None:
        if opts.mode==0 or (opts.mode==1 and self.time>=0):
            self.screen.fill("black")
            self.screen.blit(pygame.transform.scale_by(self.sprites[f"{self.scenario}scr"], glob.SF),(0,0))
            for block in self.blocks: block.render(self.screen)
            for npc in self.npcs: npc.render(self.screen)
            if opts.mode == 1:
                self.target.render(self.screen)
                self.score_cell.render(self.screen)
                self.time_cell.render(self.screen)

            angle = -self.player.tar_angle*360/(2*numpy.pi)
            compass = pygame.transform.scale_by(self.sprites["compass"], 0.3*glob.SF)
            needle  = pygame.transform.rotate(pygame.transform.scale_by(self.sprites["needle"], 0.3*glob.SF),angle)
            self.screen.blit(compass,(1200*glob.SF-compass.get_size()[0]/2,100*glob.SF-compass.get_size()[1]/2))
            self.screen.blit(needle, (1200*glob.SF- needle.get_size()[0]/2,100*glob.SF- needle.get_size()[1]/2))

            self.player.render(self.screen)
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
