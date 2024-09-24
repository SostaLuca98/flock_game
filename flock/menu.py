from flock.utils import Scene, SceneManager, Button
import pygame, time


class MenuScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, tracker, sprites: dict) -> None:
        
        super().__init__(manager, screen, tracker, sprites)
        self.previous_time = None

        # Create buttons
        self.quit_button  = Button(500, 400, "Quit Game")
        self.start_button = Button(500, 300, "Start Game")

        # Create button events
        def quit_button():  self.manager.quit = True
        #def start_button(): self.manager.set_scene("game")
        def start_button():
            self.manager.scenes["game"].build_level()
            self.manager.set_scene("game")

        self.quit_button.register_event(quit_button)
        self.start_button.register_event(start_button)

        self.buttons = [self.quit_button, self.start_button]

    def update(self) -> None:
        
        dt = self.update_time()
        mouse_x, mouse_y = pygame.mouse.get_pos() # DA CAMBIARE CON MANO

        for b in self.buttons:
            if b.hovered == False and     b.rect.collidepoint(mouse_x, mouse_y): b.hovered = True
            if b.hovered == True  and not b.rect.collidepoint(mouse_x, mouse_y): b.hovered = False

        self.quit_button.update(dt)
        self.start_button.update(dt)

    def render(self) -> None:

        self.screen.fill("black")

        self.quit_button.render(self.screen)
        self.start_button.render(self.screen)

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