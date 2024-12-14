from pygame.sprite import Sprite
from pygame.math import Vector2
from src.sprites.parents import Animation
from src.variables import GameVars


class Sakuya(Sprite, Animation):
    def __init__(self):
        super().__init__()
        self.pos = GameVars.get_center_pos()
        Animation.__init__(self, asset_id='sakuya', fps=10)

    def update(self, dt: float):
        self._update_frame(dt, scale=3)
