import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from src.sprites.parents import Animation
from src.variables import GameVars


class Sakuya(Sprite, Animation):
    def __init__(self):
        super().__init__()
        Animation.__init__(self, config_id='default', asset_id='sakuya', fps=10)
        self._update_config(
            config_id='sakuya-attack', 
            asset_id='sakuya-attack', 
            fps=12, 
            loop=False
            )
    
    def _overrides(self):
        self.pos = Vector2(GameVars.get_center_pos().x, GameVars.get_center_pos().y + 150)
        self.scale = 3.0
    
    def key_tap(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self._switch_config('sakuya-attack')

    def update(self, dt: float):
        self._update_frame(dt)
