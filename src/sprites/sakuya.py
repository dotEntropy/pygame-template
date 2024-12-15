import pygame
import json
from pygame.sprite import Sprite
from pygame.math import Vector2
from src.sprites.parents import Animation
from src.variables import GameVars


class Sakuya(Sprite, Animation):
    def __init__(self):
        super().__init__()
        Animation.__init__(self, config_id='default', asset_id='sakuya', fps=8)
        self._create_config(
            config_id='sakuya-attack', 
            asset_id='sakuya-attack', 
            fps=10, 
            loop=False
            )
    
    def _overrides(self):
        self.pos = Vector2(GameVars.get_center_pos().x-550, GameVars.get_center_pos().y + 150)
        self.scale = 2
    
    def _handle_keyframes(self):
        if self.config_id == 'sakuya-attack' and self.current_frame_idx == 0:
            self._print_current_config()
    
    def key_tap(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self._switch_config('sakuya-attack')
        if key == pygame.K_f:
            self.pos.x = GameVars.get_center_pos().x-550

    def update(self, dt: float):
        if self.config_id == 'default':
            self.pos.x += 110 * dt * self.fps / 10
            self.fps += 1 * dt
            self.configs['default']['fps'] = self.fps
        self._update_frame(dt)
