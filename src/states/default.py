import pygame
from pygame.math import Vector2
from src.states.parent import State
from src.loader import get_gfx
from src.variables import GameVars


class DefaultState(State):
    def __init__(self) -> None:
        super().__init__('default')
        self.pos = Vector2()
    
    def update(self, dt: float) -> None:
        if self.pos.x == 0:
            print(self.pos)
        self.pos.x += 100 * dt
    
    def draw(self) -> None:
        self.SCREEN.fill((0,0,0))
        self.SCREEN.blit(get_gfx('ligma'), self.pos)
    
    def handle_key_tap(self, key: int) -> None:
        if key == pygame.K_e:
            self.switch_state('state0')
            print(GameVars.states)
        if key == pygame.K_SPACE:
            self.reset_state('default')
    
    def handle_key_held(self, keys):
        pass


def setup() -> None:
    DefaultState()
