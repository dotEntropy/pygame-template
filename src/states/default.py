import pygame
from pygame.math import Vector2
from src.states.parent import State
from src.loader import get_gfx
from src.variables import GameVars
from utils.text import Text


class DefaultState(State):
    def __init__(self) -> None:
        super().__init__('default')
        self.pos = Vector2()
        self.text = Text('e')
    
    def update(self, dt: float) -> None:
        self.pos.x += 100 * dt
    
    def draw(self) -> None:
        self.SCREEN.fill((50,50,50))
        self.SCREEN.blit(get_gfx('ligma'), self.pos)
        self.text.draw() 
    
    def handle_key_tap(self, key: int) -> None:
        if key == pygame.K_e:
            self.switch_state('state0')
        if key == pygame.K_w:
            self.reset_state('default')
    
    def handle_key_held(self, keys):
        pass


def setup() -> None:
    state = DefaultState()
    print(state)
