import pygame
import colorama
from src.variables import GameVars


class State:
    def __init__(self, alias: str) -> None:
        self.alias = str(alias)
        is_reloaded = self.alias in GameVars.states
        GameVars.states[self.alias] = self
        self.SCREEN = pygame.display.get_surface()
        self._init_buttons()
        self._init_sprites()
        self._init_groups()
        load_str = 'reloaded!' if is_reloaded else 'loaded!'
        print(f'{colorama.Fore.GREEN}The state "{self.alias}" is {load_str}')

    def switch_state(self, alias: str) -> None:
        state = GameVars.states.get(alias)
        if state is None:
            print(f'{colorama.Fore.RED}State "{alias}" not found. Cannot switch.')
        else:
            GameVars.active_state = state 
    
    def reset_state(self, alias) -> None:
        state = GameVars.states.get(alias)
        if state:
            state.__init__()
        else:
            print(f'{colorama.Fore.RED}State "{alias}" not found. Cannot reset.')

    def _init_buttons(self) -> None: ... 
    def _init_sprites(self) -> None: ...
    def _init_groups(self) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self) -> None: ...
    def handle_key_tap(self, key: int) -> None: ...
    def handle_key_held(self, keys: dict) -> None: ...
    def handle_mouse_tap(self, button: int) -> None: ...
    def handle_mouse_held(self, buttons: tuple) -> None: ...
 