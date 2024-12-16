import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
from src.sprites.parents import Animation


class Button(Sprite, Animation):
    def __init__(
            self,
            func: callable,
            pos: Vector2,
            is_toggle: bool=True,
            is_instant: bool=True,
            is_pressed: bool=False,
            released_animation: dict={
                'asset_id': 'button-released-default',
                'fps': 14
                },
            pressed_animation: dict={
                'asset_id': 'button-pressed-default',
                'fps': 14
                },
            ) -> None:
        super().__init__()
        self.func = func
        self.origin_pos = pos
        self.is_toggle = is_toggle
        self.is_instant = is_instant
        self.is_pressed = is_pressed
        self.released_animation = released_animation
        self.pressed_animation = pressed_animation
        self.is_hovered = False
        self.is_press_pending = False
        self.is_m1_tapped = False
        self.is_m1_held = False
        self._load_animation_configs()
    
    def _load_animation_configs(self) -> None:
        config_id = 'released'
        asset_id = self.released_animation['asset_id']
        fps = self.released_animation['fps']
        Animation.__init__(self, config_id, asset_id, fps)

        config_id = 'pressed'
        asset_id = self.pressed_animation['asset_id']
        fps = self.pressed_animation['fps']
        loop = self.pressed_animation.get('loop', True)
        self._create_config(config_id, asset_id, fps, loop=loop)

        self.mouse_mask = pygame.mask.Mask((1, 1), fill=True)
    
    def _overrides(self) -> None:
        self.pos = self.origin_pos.copy()
        self.scale = 3

    def mouse_tap(self, button: int) -> None:
        if not self.is_toggle:
            return
        self.is_m1_tapped = button == 1
    
    def mouse_held(self, buttons: tuple[int]) -> None:
        if self.is_toggle:
            return
        self.is_m1_held = buttons[0]
    
    def update(self, *args, **kwargs) -> None:
        self._handle_presses(kwargs['mouse_pos'])
        self._update_frame(kwargs['dt'])
    
    def _handle_presses(self, mouse_pos: Vector2) -> None:
        is_last_frame_idx = self.current_frame_idx + 1 == self.total_frames
        if self.is_press_pending and is_last_frame_idx:
            self.func()
            self.is_press_pending = False

        offset = mouse_pos - self.rect.topleft
        self.is_hovered = self.mask.overlap(self.mouse_mask, offset)
        if self.is_hovered:
            self._handle_toggle()
            self._handle_held()

        if not self.is_pressed and self.config_id != 'released' and is_last_frame_idx:
            self._switch_config('released')

    def _handle_toggle(self) -> None:
        if not (self.is_toggle and self.is_m1_tapped):
            return

        self.is_m1_tapped = False

        if self.is_pressed:
            self.is_pressed = False
            return

        self._switch_config('pressed')
        self.is_pressed = True

        if self.is_instant:
            self.func()
        else:
            self.is_press_pending = True

    def _handle_held(self) -> None:
        if self.is_toggle:
            return

        if not self.is_m1_held:
            self.is_pressed = False
            return

        if not self.is_pressed:
            self.func()
            self._switch_config('pressed')
            self.is_pressed = True
