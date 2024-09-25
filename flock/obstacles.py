from .utils import Scene, SceneManager, Button
import pygame, time
from .config import args, options


class ObstScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:

        super().__init__(manager, screen, tracker, sprites)
        self.previous_time = None

        # Create buttons
        def newg():
            self.manager.scenes["game"].build_level()
            self.manager.set_scene("game")

        self.conf_butt = Button(180, 650, "Conferma").register_event(newg)
        self.ripr_butt = Button(1100, 650, "Riprova" ).register_event(lambda : print('Ripr'))

        # Create button events
        self.texts   = []
        self.buttons = [self.conf_butt, self.ripr_butt]

    def update(self) -> None:

        dt = self.update_time()
        mouse_x, mouse_y = pygame.mouse.get_pos()  # DA CAMBIARE CON MANO

        for b in self.buttons:
            if b.hovered == False and b.rect.collidepoint(mouse_x / args.SF + b.surface.get_size()[0] / 2,
                                                          mouse_y / args.SF + b.surface.get_size()[
                                                              1] / 2): b.hovered = True
            if b.hovered == True and not b.rect.collidepoint(mouse_x / args.SF + b.surface.get_size()[0] / 2,
                                                             mouse_y / args.SF + b.surface.get_size()[
                                                                 1] / 2): b.hovered = False
            b.update(dt)

    def render(self) -> None:

        self.screen.fill("black")

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