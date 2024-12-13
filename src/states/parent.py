import pygame
from src.variables import GameVars
from utils.console import print_error, print_success


class State:
    def __init__(self, alias: str) -> None:
        self.alias = str(alias)
        is_reloaded = self.alias in GameVars.states
        GameVars.states[self.alias] = self
        self.SCREEN = pygame.display.get_surface()
        self._init_sprites()
        self._init_groups()
        load_str = 'reloaded' if is_reloaded else 'loaded'
        print_success(f'The state "{self.alias}" is {load_str}!')

    def switch_state(self, alias: str) -> None:
        state = GameVars.states.get(alias)
        if state is None:
            print_error(f'State "{alias}" not found. Cannot switch.')
        else:
            GameVars.active_state = state 
    
    def reset_state(self, alias) -> None:
        state = GameVars.states.get(alias)
        if state:
            state.__init__()
        else:
            print_error(f'State "{alias}" not found. Cannot reset.')
    
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
