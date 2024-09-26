from .config import glob, args, opts
from .utils import Scene, SceneManager, Button
from .reader import Reader
import pygame, time


class ObstScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:

        super().__init__(manager, screen, tracker, sprites)
        self.previous_time = None
        self.reader = Reader()
        self.read_flag = False

        # Create buttons
        def newg():
            self.reader.quit()
            self.manager.scenes["game"].build_level()
            self.manager.set_scene("game")
        def detect():
            self.read_flag = False

        self.conf_butt = Button(180, 650, "Conferma").register_event(newg)
        self.ripr_butt = Button(1100, 650, "Riprova" ).register_event(detect)

        # Create button events
        self.texts   = []
        self.buttons = [self.conf_butt, self.ripr_butt]

    def update(self) -> None:

        dt = self.update_time()
        mouse_x, mouse_y = pygame.mouse.get_pos()  # DA CAMBIARE CON MANO

        for b in self.buttons:
            if b.hovered == False and b.rect.collidepoint(mouse_x / glob.SF + b.surface.get_size()[0] / 2,
                                                          mouse_y / glob.SF + b.surface.get_size()[
                                                              1] / 2): b.hovered = True
            if b.hovered == True and not b.rect.collidepoint(mouse_x / glob.SF + b.surface.get_size()[0] / 2,
                                                             mouse_y / glob.SF + b.surface.get_size()[
                                                                 1] / 2): b.hovered = False
            b.update(dt)

        if not self.read_flag:
            self.read_flag = True
            self.reader.detect()

    def render(self) -> None:

        self.screen.fill("black")

        for x,y,r in zip(self.reader.x_centers, self.reader.y_centers, self.reader.radii):
            pygame.draw.circle(self.screen, (0,255,0), (x*glob.SF, y*glob.SF), r*glob.SF)
            pygame.draw.circle(self.screen, (255,0,0), (x*glob.SF, y*glob.SF), 7*glob.SF)
        if opts.mode == 1:
            target = self.manager.scenes["game"].target
            pygame.draw.circle(self.screen, (0, 0, 255), (target.x*glob.SF, target.y*glob.SF), target.r*glob.SF)

        for b in self.buttons:
            b.render(self.screen)
        for t in self.texts:
            t.render(self.screen)

        pygame.display.update()

    def poll_events(self) -> None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reader.quit()
                self.manager.quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.reader.quit()
                self.manager.quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reader.quit()
                self.manager.set_scene("game")

            # Mouse detection DA CAMBIARE CON MANO
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in self.buttons:
                    if b.hovered:
                        b.event()