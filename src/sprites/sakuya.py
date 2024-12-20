import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from src.sprites.parents import Animation
from src.variables import GameVars


class TestSprite(Sprite, Animation):
    def __init__(self):
        super().__init__()
        Animation.__init__(self, config_id='test', asset_id='test', fps=2)
        self._create_config(
            config_id='alt-test', 
            asset_id='alt-test', 
            fps=2,
            loops=1
            )
    
    def _overrides(self):
        self.pos = Vector2(GameVars.get_center_pos().x-550, GameVars.get_center_pos().y + 150)
        self.scale = 2
    
    def _handle_keyframes(self):
        if self.config_id == 'alt-test' and self.current_frame_idx == 0:
            pass
            # self._print_current_config()
    
    def key_tap(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self._switch_config('alt-test')
        if key == pygame.K_f:
            self.pos.x = GameVars.get_center_pos().x-550

    def update(self, *args, **kwargs) -> None:
        self._update_frame(kwargs['dt'])
