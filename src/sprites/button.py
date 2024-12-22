import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite
from src.sprites.parents import Animation


class Button(Sprite, Animation):
    def __init__(
            self,
            func: callable,
            pos: Vector2,
            scale: float=1.0,
            is_toggle: bool=True,
            is_disabled: bool=False,
            is_instant: bool=True,
            is_pressed: bool=False,
            released_animation: dict={
                'asset_id': 'button-released',
                'fps': 14
                },
            hovered_animation: dict={
                'asset_id': 'button-hovered',
                'fps': 14
                },
            pressed_animation: dict={
                'asset_id': 'button-pressed',
                'fps': 14
                },
            ) -> None:
        super().__init__()
        self.func = func
        self.ORIGIN_POS = pos
        self.ORIGIN_SCALE = scale
        self.is_toggle = is_toggle
        self.is_disabled = is_disabled
        self.is_instant = is_instant
        self.is_pressed = is_pressed
        self.released_animation = released_animation
        self.hovered_animation = hovered_animation
        self.pressed_animation = pressed_animation
        self.is_hovered = False
        self.is_hovered_on_click = False
        self.is_activation_pending = False
        self.is_delayed_activation_pending = False
        self.is_release_pending = False
        self.is_m1_held = False
        self.is_m1_released = False
        self.is_mouse_pos_locked = False
        self._load_animation_configs()
    
    def _load_animation_configs(self) -> None:
        config_id = 'released'
        asset_id = self.released_animation.get('asset_id', 'button-released')
        fps = self.released_animation.get('fps', 14)
        Animation.__init__(self, config_id, asset_id, fps)

        config_id = 'hovered'
        asset_id = self.hovered_animation.get('asset_id', 'button-hovered')
        fps = self.hovered_animation.get('fps', 14)
        self._create_config(config_id, asset_id, fps)

        config_id = 'pressed'
        asset_id = self.pressed_animation.get('asset_id', 'button-pressed')
        fps = self.pressed_animation.get('fps', 14)
        self._create_config(config_id, asset_id, fps)
    
    def _overrides(self) -> None:
        self.pos = self.ORIGIN_POS.copy()
        self.scale = self.ORIGIN_SCALE
    
    def mouse_held(self, buttons: tuple[int]) -> None:
        self.is_m1_held = buttons[0]
    
    def update(self, *args, **kwargs) -> None:
        self._handle_presses(kwargs['mouse_pos'])
        self._update_frame(kwargs['dt'])
    
    def _handle_presses(self, mouse_pos: Vector2) -> None:
        self.is_hovered = self.rect.collidepoint(*mouse_pos)

        self._handle_m1_release()
        self._handle_m1_lock()

        if self.is_toggle:
            self._handle_toggle_press()
            self._handle_toggle_animation_switch()
        else:
            self._handle_normal_press()
            self._handle_normal_animation_switch()

        self._handle_activation()
        self._handle_pending_activation() 
        self.is_m1_released = False

    def _handle_m1_lock(self) -> None:
        if self.is_m1_released:
            self.is_mouse_pos_locked = False
            return

        if self.is_m1_held and not self.is_mouse_pos_locked:
            self.is_hovered_on_click = self.is_hovered
            self.is_mouse_pos_locked = True
    
    def _handle_m1_release(self) -> None:
        if self.is_m1_held and not self.is_release_pending:
            self.is_release_pending = True
        
        if not self.is_m1_held and self.is_release_pending:
            self.is_m1_released = True
            self.is_release_pending = False
    
    def _handle_pending_activation(self) -> None:
        self.is_last_frame_idx = self.current_frame_idx + 1 == self.total_frames
        if self.is_delayed_activation_pending and self.is_last_frame_idx:
            self.func()
            self.is_delayed_activation_pending = False

    def _handle_toggle_animation_switch(self) -> None:
        if self.is_pressed and self.config_id != 'pressed':
            self._switch_config('pressed')
        elif not self.is_pressed and self.is_hovered and self.config_id != 'hovered':
            self._switch_config('hovered')
        elif not self.is_hovered and self.config_id not in ('pressed', 'released'):
            self._switch_config('released')

    def _handle_toggle_press(self) -> None:
        press_conditions = (
            self.is_hovered_on_click,
            self.is_m1_released,
            self.is_hovered
        )
        if all(press_conditions) and not self.is_pressed:
            self.is_activation_pending = True
            self.is_pressed = True
        elif all(press_conditions) and self.is_pressed:
            self.is_pressed = False
    
    def _handle_normal_animation_switch(self) -> None:
        if self.is_pressed and self.config_id != 'pressed':
            self._switch_config('pressed')
        elif not self.is_pressed and self.is_hovered and self.config_id != 'hovered':
            self._switch_config('hovered')
        elif not self.is_pressed and not self.is_hovered and self.config_id != 'released':
            self._switch_config('released')

    def _handle_normal_press(self) -> None:
        press_conditions = (
            self.is_hovered_on_click,
            self.is_hovered,
            self.is_m1_held
        )
        if all(press_conditions):
            self.is_pressed = True
        else:
            self.is_pressed = False

    def _handle_activation(self) -> None:
        activate_conditions = (
            self.is_hovered_on_click,
            self.is_hovered,
            self.is_m1_released,
        )
        if all(activate_conditions):
            self._activate()
    
    def _activate(self) -> None:
        if self.is_instant:
            self.func()
        else:
            self.is_delayed_activation_pending = True
