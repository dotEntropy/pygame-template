import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from src.sprites.parents import Animation
from src.variables import GameVars


class StockSprite(Sprite, Animation):
    def __init__(self):
        super().__init__()
        Animation.__init__(self, config_id='test', asset_id='test', fps=3)
        self._create_config(
            config_id='test_', 
            asset_id='test_', 
            fps=5,
            loops=2
            )
    
    def _overrides(self):
        self.pos = Vector2(100, 100)
        self.scale = 1
    
    def _handle_keyframes(self):
        return super()._handle_keyframes()
    
    def key_tap(self, key: int) -> None:
        if key == pygame.K_SPACE and self.config_id != 'test_':
            self._switch_config('test_')
        if key == pygame.K_f:
            self.pos.x = GameVars.get_center_pos().x - 550

    def update(self, *args, **kwargs) -> None:
        self._update_frame(kwargs['dt'])
