from utils import Scene, SceneManager
import pygame, time

class Button:
    def __init__(self,
                 x, y,
                 text: str) -> None:
        self.x = x
        self.y = y
        
        self.font = pygame.font.SysFont("Calibri", 36)
        self.color = "white"
        self.text = text

        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.hovered = False

        self.event = lambda: print("Default button")

    def update(self, dt):
        if self.hovered is True:
            self.color = "blue"
        else:
            self.color = "white"

        self.text_surface = self.font.render(self.text, True, self.color)

    def set_hover(self, hovered: bool):
        self.hovered = hovered

    def register_event(self, func):
        self.event = func

    def render(self, screen: pygame.Surface):
        screen.blit(self.text_surface, (self.x, self.y))

class MenuScene(Scene):

    def __init__(self, manager: SceneManager, screen: pygame.Surface, sprites: dict) -> None:
        
        super().__init__(manager, screen, sprites)
        self.previous_time = None

        # Create buttons
        self.quit_button  = Button(500, 400, "Quit Game")
        self.start_button = Button(500, 300, "Start Game")

        # Create button events
        def quit_button():  self.manager.quit = True
        def start_button(): self.manager.set_scene("game")

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.manager.set_scene("game")

            # Mouse detection DA CAMBIARE CON MANO
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in self.buttons:
                    if b.hovered:
                        b.event()