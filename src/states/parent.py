import pygame
from src.variables import GameVars
from utils.colored_print import print_error, print_success


class State:
    def __init__(self, alias: str) -> None:
        try:
            GameVars.states[alias] = self
            self.alias = alias
            self.SCREEN = pygame.display.get_surface()
            self._init_sprites()
            self._init_groups()
            print_success(f'The state "{self.alias}" is loaded!')
        except AttributeError:
            print('Specify a valid state alias.')

    def switch_state(self, alias: str) -> None:
        state = GameVars.states.get(alias)
        if state is None:
            print_error(f'State {alias} not found. Cannot switch.')
        else:
            GameVars.active_state = state 
    
    def reset_state(self, alias) -> None:
        state = GameVars.states.get(alias)
        if state:
            state.__init__()
        else:
            print_error(f'State {alias} not found. Cannot reset.')
    
    def _init_sprites(self) -> None:
        pass
    
    def _init_groups(self) -> None:
        pass
    
    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pass
    
    def handle_key_tap(self, key: int) -> None:
        pass

    def handle_key_held(self, keys: dict) -> None:
        pass

    def handle_mouse_tap(self, button: int) -> None:
        pass

    def handle_mouse_held(self, buttons: tuple) -> None:
        pass
