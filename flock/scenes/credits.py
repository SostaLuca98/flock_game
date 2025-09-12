from ..config import glob, args, opts
from ..utils import Scene, SceneManager, Button
import pygame, time


class CreditScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:
        
        super().__init__(manager, screen, tracker, sprites)
        self.previous_time = None

        # Create buttons
        self.menu_button = Button(1150, 650, "Menu").register_event(lambda : self.manager.set_scene("menu"))

        self.buttons = [self.menu_button]

    def update(self) -> None:
        
        dt = self.update_time()
        mouse_x, mouse_y = pygame.mouse.get_pos() # DA CAMBIARE CON MANO

        for b in self.buttons:
            if b.hovered == False and     b.rect.collidepoint(mouse_x/glob.SF+b.surface.get_size()[0]/2, mouse_y/glob.SF+b.surface.get_size()[1]/2): b.hovered = True
            if b.hovered == True  and not b.rect.collidepoint(mouse_x/glob.SF+b.surface.get_size()[0]/2, mouse_y/glob.SF+b.surface.get_size()[1]/2): b.hovered = False
            b.update(dt)

    def render(self) -> None:

        self.screen.fill("black")


        SW, SH = glob.SW, glob.SH
        logo = pygame.transform.scale_by(self.sprites["logo"], glob.SF)
        self.screen.blit(logo,(SW/2*glob.SF-logo.get_rect().width/2,SH/2*glob.SF-logo.get_rect().height/2))

        for b in self.buttons:
            b.render(self.screen)

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