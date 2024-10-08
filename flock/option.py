import copy

from .config import glob, args, opts, default_bird, default_fish, default_sheep
from .utils import Scene, SceneManager, Button
import pygame, time

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

        # Modality
        self.mode_1 = Button(550, 576, "", pygame.transform.scale_by(sprites[f"mode0"], 0.12)).register_event(lambda : setattr(opts, 'mode', 0))
        self.mode_2 = Button(750, 576, "", pygame.transform.scale_by(sprites[f"mode1"], 0.12)).register_event(lambda : setattr(opts, 'mode', 1))

        self.menu_button = Button(1150, 650, "Menu")
        def menu_button(): self.manager.set_scene("menu")
        self.menu_button.register_event(menu_button)

        # Create button events

        self.texts   = [self.scen_text, self.diff_text, self.obst_text, self.mode_text]
        self.buttons = [self.menu_button,
                        self.scen_1, self.scen_2, self.scen_3,
                        self.diff_1, self.diff_2, self.diff_3,
                        self.obst_1, self.obst_2,
                        self.mode_1, self.mode_2]

    def update(self) -> None:

        dt = self.update_time()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for b in self.buttons:
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

        for b in self.buttons:
            b.render(self.screen)
        for t in self.texts:
            t.render(self.screen)

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
                for b in self.buttons:
                    if b.hovered:
                        b.event()
    @staticmethod
    def set_values(sender, receiver):
        for campo in sender.__dataclass_fields__:
            setattr(receiver, campo, getattr(sender, campo))

    @staticmethod
    def change_settings():
        if   opts.scen == 0: OptiScene.set_values(default_bird,  args)
        elif opts.scen == 1: OptiScene.set_values(default_fish,  args)
        elif opts.scen == 2: OptiScene.set_values(default_sheep, args)
        if opts.diff == 0:
            pass
        if opts.diff == 1:
            args.speed *= 2
            args.rot   *= 0.9
            args.t_max *= 0.75
        if opts.diff == 2:
            args.speed *= 4
            args.rot   *= 0.7
            args.t_max *= 0.5
