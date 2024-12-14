import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from src.sprites.parents import Animation
from src.variables import GameVars


class Sakuya(Sprite, Animation):
    def __init__(self):
        super().__init__()
        Animation.__init__(self, asset_id='sakuya', fps=20)
    
    def _overrides(self):
        self.pos = GameVars.get_center_pos()
        self.scale = 3.0
    
    def key_tap(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self._update_frames('sakuya', fps=20, reset_idx=False)
        if key == pygame.K_v:
            self._update_frames('sakuya', fps=10, reset_idx=False)

    def update(self, dt: float):
        self._update_frame(dt)
