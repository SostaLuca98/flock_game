from ..config import glob, levels, opts, default_bird, default_fish, default_human, default_abstr
from ..utils import Scene, SceneManager, Button
import pygame

class OptiScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:

        super().__init__(manager, screen, tracker, sprites)
        self.previous_time = None

        # Create buttons
        self.scen_text = Button(240, 144, "Scenario")
        self.diff_text = Button(240, 288, "Difficoltà")
        self.obst_text = Button(240, 432, "Ostacoli")
        self.mode_text = Button(240, 576, "Modalità")

        # Scenarios
        self.scen_1 = Button(550, 144, "", pygame.transform.scale_by(sprites[f"scen0"], 0.12)).register_event(lambda : setattr(opts, 'scen', 0))
        self.scen_2 = Button(750, 144, "", pygame.transform.scale_by(sprites[f"scen1"], 0.12)).register_event(lambda : setattr(opts, 'scen', 1))
        self.scen_3 = Button(950, 144, "", pygame.transform.scale_by(sprites[f"scen2"], 0.12)).register_event(lambda : setattr(opts, 'scen', 2))

        # Difficulties
        self.diff_1 = Button(550, 288, "", pygame.transform.scale_by(sprites[f"diff0"], 0.12)).register_event(lambda : setattr(opts, 'diff', 0))
        self.diff_2 = Button(750, 288, "", pygame.transform.scale_by(sprites[f"diff1"], 0.12)).register_event(lambda : setattr(opts, 'diff', 1))
        self.diff_3 = Button(950, 288, "", pygame.transform.scale_by(sprites[f"diff2"], 0.12)).register_event(lambda : setattr(opts, 'diff', 2))

        # Obstacles
        self.obst_1 = Button(550, 432, "", pygame.transform.scale_by(sprites[f"obst0"], 0.12)).register_event(lambda : setattr(opts, 'obst', 0))
        self.obst_2 = Button(750, 432, "", pygame.transform.scale_by(sprites[f"obst1"], 0.12)).register_event(lambda : setattr(opts, 'obst', 1))
        self.obst_3 = Button(950, 432, "", pygame.transform.scale_by(sprites[f"obst2"], 0.12)).register_event(lambda : setattr(opts, 'obst', 2))

        # Modality
        def abstr_func(): 
            setattr(opts, 'mode', 2) 
            setattr(opts, 'scen', 3)
        self.mode_1 = Button(550, 576, "", pygame.transform.scale_by(sprites[f"mode0"], 0.12)).register_event(lambda : setattr(opts, 'mode', 0))
        self.mode_2 = Button(750, 576, "", pygame.transform.scale_by(sprites[f"mode1"], 0.12)).register_event(lambda : setattr(opts, 'mode', 1))
        self.mode_3 = Button(950, 576, "", pygame.transform.scale_by(sprites[f"mode2"], 0.12)).register_event(abstr_func)
  
        self.temp_1 = Button(1150, 144, "200", font=("Aptos", 32)).register_event(lambda : setattr(opts, 'temp', 4))
        self.temp_2 = Button(1150, 224, "100", font=("Aptos", 32)).register_event(lambda : setattr(opts, 'temp', 3))
        self.temp_3 = Button(1150, 304,  "50", font=("Aptos", 32)).register_event(lambda : setattr(opts, 'temp', 2))
        self.temp_4 = Button(1150, 384,  "25", font=("Aptos", 32)).register_event(lambda : setattr(opts, 'temp', 1))
        self.temp_5 = Button(1150, 464,  "10", font=("Aptos", 32)).register_event(lambda : setattr(opts, 'temp', 0))

        self.bigobs_pos_nw = Button(1050, 412, "NW", pygame.transform.scale_by(sprites[f"posNW"], 0.2)).register_event(lambda : setattr(opts, 'bigobs_pos', 11))
        self.bigobs_pos_nc = Button(1110, 412, "NC", pygame.transform.scale_by(sprites[f"posNC"], 0.2)).register_event(lambda : setattr(opts, 'bigobs_pos', 5))
        self.bigobs_pos_ne = Button(1170, 412, "NE", pygame.transform.scale_by(sprites[f"posNE"], 0.2)).register_event(lambda : setattr(opts, 'bigobs_pos', 12))
        # self.bigobs_pos_sw = Button(1050, 472, "SW", pygame.transform.scale_by(sprites[f"posSW"], 0.2)).register_event(lambda : setattr(opts, 'bigobs_pos', 21))
        self.bigobs_empty_sw = Button(1050, 472, "SW", pygame.transform.scale_by(sprites[f"emptySW"], 0.2))
        self.bigobs_pos_sc = Button(1110, 472, "SC", pygame.transform.scale_by(sprites[f"posSC"], 0.2)).register_event(lambda : setattr(opts, 'bigobs_pos', 5))
        self.bigobs_pos_se = Button(1170, 472, "SE", pygame.transform.scale_by(sprites[f"posSE"], 0.2)).register_event(lambda : setattr(opts, 'bigobs_pos', 22))

        self.menu_button = Button(1150, 650, "Menu").register_event(lambda : self.manager.set_scene("menu"))

        self.texts   = [self.scen_text, self.diff_text, self.obst_text, self.mode_text]
        self.buttons = [self.menu_button,
                        self.scen_1, self.scen_2, self.scen_3,
                        self.diff_1, self.diff_2, self.diff_3,
                        self.obst_1, self.obst_2, self.obst_3,
                        self.mode_1, self.mode_2, self.mode_3]
        self.temps = [self.temp_1, self.temp_2, self.temp_3, self.temp_4, self.temp_5]
        self.bigobs_poss = [self.bigobs_pos_nw, self.bigobs_pos_nc, self.bigobs_pos_ne, self.bigobs_empty_sw, self.bigobs_pos_sc, self.bigobs_pos_se]

    def update(self) -> None:

        dt = self.update_time()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for b in self.buttons+self.temps+self.bigobs_poss:
            if b.hovered == False and b.rect.collidepoint(mouse_x / glob.SF + b.surface.get_size()[0] / 2,
                                                          mouse_y / glob.SF + b.surface.get_size()[
                                                              1] / 2): b.hovered = True
            if b.hovered == True and not b.rect.collidepoint(mouse_x / glob.SF + b.surface.get_size()[0] / 2,
                                                             mouse_y / glob.SF + b.surface.get_size()[
                                                                 1] / 2): b.hovered = False
            b.update(dt)

    def render(self) -> None:

        self.screen.fill("black")
        W, H = self.scen_1.rect.width*1.4*glob.SF, self.scen_1.rect.height*1.4*glob.SF
        pygame.draw.rect(self.screen, (0, 0, 255), ((550 + 200 * opts.scen)*glob.SF - W / 2, 144*glob.SF - H / 2, W, H))
        pygame.draw.rect(self.screen, (0, 0, 255), ((550 + 200 * opts.diff)*glob.SF - W / 2, 288*glob.SF - H / 2, W, H))
        pygame.draw.rect(self.screen, (0, 0, 255), ((550 + 200 * opts.obst)*glob.SF - W / 2, 432*glob.SF - H / 2, W, H))
        pygame.draw.rect(self.screen, (0, 0, 255), ((550 + 200 * opts.mode)*glob.SF - W / 2, 576*glob.SF - H / 2, W, H))
        
        if opts.scen == 3:
            pygame.draw.rect(self.screen, (0, 0, 0), ((550 + 200 * opts.scen)*glob.SF - W / 2, 144*glob.SF - H / 2, W, H))

        if opts.mode == 2 and opts.scen == 3:
            w, h = 50*glob.SF, 80*glob.SF

            thick = 1.4
            r = 50*glob.SF
            pygame.draw.circle(self.screen, (255, 255, 255), (1150*glob.SF, 144*glob.SF + 5*h-r*1.2/4), r*1.2)
            pygame.draw.rect(self.screen, (255, 255, 255), (1150*glob.SF - thick*w / 2, 144*glob.SF - thick*h/2 + 5*glob.SF, thick*w, thick*4*h))

            for i in range(5):
                color = (0,0,0) if i>opts.temp else (255,0,0)
                pygame.draw.rect(self.screen, color, (1150*glob.SF - w / 2, 144*glob.SF - h / 2 + (4-i)*h, w, h))
            for i in range(1,5):
                pygame.draw.rect(self.screen, (0, 0, 0), (1150*glob.SF, 144*glob.SF - h / 2 + i*h - h/15, w/2, h/15))
            pygame.draw.circle(self.screen, (255, 0, 0), (1150*glob.SF, 144*glob.SF + 5*h-r/2+10*glob.SF), r)

        if opts.obst == 1 and opts.scen == 1: # TODO: here we set bigobs in any fish case: consider allowing both custom obst and bigobs, as separate options
            w, h = 30*glob.SF, 30*glob.SF
            if opts.bigobs_pos > 0:
                if opts.bigobs_pos == 5:
                    pygame.draw.rect(self.screen, (0, 0, 255), (1110*glob.SF - w / 2, 442*glob.SF - h / 2, w, h))
                else:
                    pygame.draw.rect(self.screen, (0, 0, 255), ( ( 1037 + 147*(opts.bigobs_pos % 10 - 1) )*glob.SF - w / 2, ( 399 + 86*(opts.bigobs_pos // 10 - 1) )*glob.SF - h / 2, w, h))

        for b in self.buttons:
            b.render(self.screen)
        for t in self.texts:
            t.render(self.screen)
        for t in self.temps:
            if opts.mode == 2 and opts.scen == 3: t.render(self.screen)
        for t in self.bigobs_poss:
            if opts.obst == 1 and opts.scen == 1: t.render(self.screen)

        pygame.display.update()

    def poll_events(self) -> None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.manager.quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.manager.set_scene("game")

            # Mouse detection DA CAMBIARE CON MANO
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in self.buttons+self.temps+self.bigobs_poss:
                    if b.hovered:
                        b.event()
    @staticmethod
    def set_values(sender, receiver):
        for campo in sender.__dataclass_fields__:
            setattr(receiver, campo, getattr(sender, campo))

    @staticmethod
    def change_settings():
        if   opts.scen == 0: OptiScene.set_values(default_bird,  levels)
        elif opts.scen == 1: OptiScene.set_values(default_fish,  levels)
        elif opts.scen == 2: OptiScene.set_values(default_human, levels)
        elif opts.scen == 3: OptiScene.set_values(default_abstr, levels)
        if opts.diff == 0:
            pass
        if opts.diff == 1:
            levels.speed *= 2
            levels.rot   *= 0.9
            levels.t_max *= 0.75
        if opts.diff == 2:
            levels.speed *= 4
            levels.rot   *= 0.7
            levels.t_max *= 0.5
        if opts.mode == 2 and opts.scen == 3:
            if opts.temp == 0: levels.n = 10
            if opts.temp == 1: levels.n = 25
            if opts.temp == 2: levels.n = 50
            if opts.temp == 3: levels.n = 100
            if opts.temp == 4: levels.n = 200
