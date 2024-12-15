import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
from src.loader import get_gfx
from src.sprites.parents import Graphics, Animation


class Button(Sprite, Animation):
    def __init__(
            self,
            func: callable,
            pos: Vector2,
            asset_id: str,
            is_toggle: bool,
            is_loop_toggle: bool=False,
            is_pressed: bool=False,
            is_disabled: bool=False,
            is_animated: bool=False,
            config_id: str | None=None,
            fps: int | None=None
            ) -> None:
        super().__init__()
        self.func = func
        self.origin_pos = pos
        self.asset_id = asset_id
        self.is_toggle = is_toggle
        self.is_pressed = is_pressed
        self.is_disabled = is_disabled
        self.is_animated = is_animated
        self.config_id = config_id
        self.fps = fps
        if is_animated and config_id and fps:
            Animation.__init__(self, config_id, asset_id, fps)
        else:
            Graphics.__init__(self)
    
    def _overrides(self) -> None:
        self.pos = self.origin_pos.copy()
    
    def update(self, dt: float) -> None:
        if self.is_animated:
            self._update_frame(dt)
        if self.is_pressed:
            self.func()
            self.is_pressed = False
    
    def mouse_tap(self, button: int) -> None:
        if button == 1:
            self.is_pressed = True

    def mouse_held(self, buttons: tuple[int]) -> None:
        ...
