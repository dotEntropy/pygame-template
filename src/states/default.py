import pygame
from pygame.math import Vector2
from src.states.parent import State
from utils.text import Text
from src.sprites.templates import Button
from src.variables import GameVars
from src.sprites.stock_sprite import StockSprite


class DefaultState(State):
    def __init__(self) -> None:
        super().__init__('default')

    def _init_sprites(self):
        self.stock_sprite = StockSprite()
        self.button = Button(
            self.say,
            Vector2(100, 200), 
            scale=0.25,
            is_toggle=False, 
            released_animation={
                'asset_id': 'button-release',
                },
            hovered_animation={
                'asset_id': 'button-hover',
            },
            pressed_animation={
                'asset_id': 'button-press',
                },
            )

    def _init_groups(self):
        self.group = pygame.sprite.Group()
        self.group.add(self.stock_sprite, self.button)
    
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
