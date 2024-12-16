import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from src.sprites.parents import Animation
from src.variables import GameVars


class Sakuya(Sprite, Animation):
    def __init__(self):
        super().__init__()
        Animation.__init__(self, config_id='sakuya', asset_id='sakuya', fps=12)
        self._create_config(
            config_id='sakuya-attack', 
            asset_id='sakuya-attack', 
            fps=16,
            loop=False
            )
    
    def _overrides(self):
        self.pos = Vector2(GameVars.get_center_pos().x-550, GameVars.get_center_pos().y + 150)
        self.scale = 2
    
    def _handle_keyframes(self):
        if self.config_id == 'sakuya-attack' and self.current_frame_idx == 0:
            pass
            # self._print_current_config()
    
    def key_tap(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self._switch_config('sakuya-attack')
        if key == pygame.K_f:
            self.pos.x = GameVars.get_center_pos().x-550

    def update(self, *args, **kwargs) -> None:
        self._update_frame(kwargs['dt'])
