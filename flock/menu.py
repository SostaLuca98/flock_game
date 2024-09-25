from .utils import Scene, SceneManager, Button
import pygame, time
from .config import args, options


class MenuScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:
        
        super().__init__(manager, screen, tracker, sprites)
        self.previous_time = None

        # Create buttons
        self.newg_button = Button(640, 144, "Nuovo Gioco")
        self.cont_button = Button(640, 288, "Continua Gioco")
        self.opti_button = Button(640, 432, "Opzioni")
        self.quit_button = Button(640, 576, "Esci")

        # Create button events
        def newg_button():
            if options.obst == 1:
                self.manager.set_scene("obst")
                self.manager.scenes["obst"].reader.open()
                self.manager.scenes["obst"].reader.detect()
            else:
                self.manager.scenes["game"].build_level()
                self.manager.set_scene("game")
                
        def cont_button(): self.manager.set_scene("game")
        def opti_button(): self.manager.set_scene("opti")
        def quit_button():  self.manager.quit = True

        self.newg_button.register_event(newg_button)
        self.cont_button.register_event(cont_button)
        self.opti_button.register_event(opti_button)
        self.quit_button.register_event(quit_button)

        self.buttons = [self.newg_button, self.cont_button, self.opti_button, self.quit_button]

    def update(self) -> None:
        
        dt = self.update_time()
        mouse_x, mouse_y = pygame.mouse.get_pos() # DA CAMBIARE CON MANO

        for b in self.buttons:
            if b.hovered == False and     b.rect.collidepoint(mouse_x/args.SF+b.surface.get_size()[0]/2, mouse_y/args.SF+b.surface.get_size()[1]/2): b.hovered = True
            if b.hovered == True  and not b.rect.collidepoint(mouse_x/args.SF+b.surface.get_size()[0]/2, mouse_y/args.SF+b.surface.get_size()[1]/2): b.hovered = False
            b.update(dt)

    def render(self) -> None:

        self.screen.fill("black")

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