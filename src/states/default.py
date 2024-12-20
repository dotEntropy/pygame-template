import pygame
from pygame.math import Vector2
from src.states.parent import State
from utils.text import Text
from src.variables import GameVars
from src.sprites.sakuya import TestSprite
from src.sprites.button import Button


class DefaultState(State):
    def __init__(self) -> None:
        super().__init__('default')

    def _init_sprites(self):
        self.sakuya = TestSprite()
        self.button = Button(
            self.say,
            GameVars.get_center_pos(), 
            is_toggle=False, 
            released_animation={
                'asset_id': 'button-release',
                'fps': 14
                },
            hovered_animation={
                'asset_id': 'button-hover',
                'fps': 14
            },
            pressed_animation={
                'asset_id': 'button-hover',
                'fps': 14
                },
            )

    def _init_groups(self):
        self.group = pygame.sprite.Group()
        self.group.add(self.sakuya, self.button)
    
    def say(self) -> None:
        print(pygame.mouse.get_pos())
    
    def update(self, dt: float) -> None:
        mouse_pos = Vector2(pygame.mouse.get_pos())
        self.group.update(dt=dt, mouse_pos=mouse_pos)
    
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
