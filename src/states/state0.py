import pygame
from src.states.parent import State
from src.loader import get_gfx
from src.variables import GameVars


class State0(State):
    def __init__(self) -> None:
        super().__init__('state0')
        self.count = 0
    
    def draw(self) -> None:
        self.SCREEN.fill((0,0,0))
        self.count += 1
        print(self.count)
    
    def handle_key_tap(self, key: int) -> None:
        if key == pygame.K_e:
            self.switch_state('default')
    
    def handle_key_held(self, keys):
        pass

def setup() -> None:
    State0()
    