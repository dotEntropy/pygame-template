from pygame.sprite import Sprite
from pygame.math import Vector2
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


import pygame
from src.loader import get_font


class Text:
    def __init__(
        self,
        texts: list[str]="",
        family: str="default",
        size: int=20,
        pos: Vector2=Vector2(20, 20),
        color: tuple[int, int, int]=(255, 255, 255),
        spacing: int | float=5,
        aa: bool=True,
        bg_color: tuple[int, int, int] | None=None
        ) -> None:
        self.display = pygame.display.get_surface()
        self.texts = texts if type(texts) is list else ['change to list']
        self.update_font(family, size)
        self.pos = pos
        self.color = color
        self.spacing = spacing
        self.aa = aa
        self.bg_color = bg_color
    
    def update(
        self, 
        texts: list[str] | None=None, 
        pos: Vector2 | None=None,
        color: tuple[int] | None=None,
        spacing: float | None=None,
        aa: bool | None=None,
        bg_color: tuple[int, int, int] | None=None
        ) -> None:
        self._update_texts(texts)
        self._update_pos(pos)
        self._update_color(color)
        self._update_aa(aa)
        self._update_bg_color(bg_color)
        self._update_spacing(spacing)
    
    def update_font(self, family: str | None=None, size: int | None=None) -> None:
        if not (family or size) or not type(size) is int:
            return
        self.size = size if size else self.size
        self.family = family if family else self.family
        self.font = get_font(family, size)
    
    def _update_texts(self, texts: list[str] | None) -> None:
        if self.texts == texts or type(texts) is not list: 
            return
        self.texts = texts
    
    def _update_pos(self, pos: Vector2 | None) -> None:
        if self.pos == pos or pos is None: 
            return
        self.pos = pos.copy()
    
    def _update_color(self, color: tuple[int] | None) -> None:
        if self.color == color or color is None: 
            return
        self.color = color
    
    def _update_spacing(self, spacing: int | float) -> None:
        if self.spacing == spacing or spacing is None: 
            return
        self.spacing = spacing
    
    def _update_aa(self, aa: bool) -> None:
        if self.aa == aa or aa is None: 
            return
        self.aa = aa
    
    def _update_bg_color(self, bg_color: tuple[int, int, int] | None) -> None:
        if self.bg_color == bg_color or bg_color is None: 
            return
        self.bg_color = bg_color

    def draw(self):
        x_pos = self.pos.x
        y_pos = self.pos.y
        for text in self.texts:
            self.surface = self.font.render(text, self.aa, self.color, self.bg_color)
            self.display.blit(self.surface, [x_pos, y_pos])
            y_pos += self.size + self.spacing
