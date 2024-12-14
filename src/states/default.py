import pygame
from src.states.parent import State
from utils.text import Text
from src.variables import GameVars
from src.sprites.sakuya import Sakuya


class DefaultState(State):
    def __init__(self) -> None:
        super().__init__('default')

    def _init_groups(self):
        self.group = pygame.sprite.Group()

    def _init_sprites(self):
        self.sakuya = Sakuya()
        self.group.add(self.sakuya)
    
    def update(self, dt: float) -> None:
        self.group.update(dt)
    
    def draw(self) -> None:
        self.SCREEN.fill((50,50,50))
        self.group.draw(self.SCREEN)
    
    def handle_key_tap(self, key: int) -> None:
        if key == pygame.K_e:
            self.switch_state('state0')
        if key == pygame.K_w:
            self.reset_state('default')
    
    def handle_key_held(self, keys):
        pass


def setup() -> None:
    DefaultState()
