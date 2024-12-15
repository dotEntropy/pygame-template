import pygame
from src.states.parent import State
from utils.text import Text
from src.variables import GameVars
from src.sprites.sakuya import Sakuya
from src.sprites.button import Button


class DefaultState(State):
    def __init__(self) -> None:
        super().__init__('default')

    def _init_groups(self):
        self.group = pygame.sprite.Group()

    def _init_sprites(self):
        self.sakuya = Sakuya()
        # self.button = Button(
        #     print('Pressed!'), 
        #     GameVars.get_center_pos(), 
        #     'sakuya', 
        #     is_toggle=False, 
        #     is_animated=True, 
        #     config_id='button',
        #     fps=10
        #     )
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
        
        for sprites in self.group.sprites():
            sprites.key_tap(key)

    def handle_key_held(self, keys: pygame.key.ScancodeWrapper) -> None:
        for sprites in self.group.sprites():
            sprites.key_held(keys)
    
    def handle_mouse_tap(self, button: int) -> None:
        for sprites in self.group.sprites():
            sprites.mouse_tap(button)

    def handle_mouse_held(self, buttons: tuple[int]) -> None:
        for sprites in self.group.sprites():
            sprites.mouse_held(buttons)
    


def setup() -> None:
    DefaultState()
