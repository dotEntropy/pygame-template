import pygame
import json
import colorama
from pygame.math import Vector2
from pygame.sprite import Sprite
from src.loader import get_gfx
from src.variables import GameVars


class Graphics:
    def __init__(self) ->None:
        self.pos = Vector2()
        self.scale = 1.0
        self.angle_deg = 0
        self._overrides()
    
    def _overrides(self) -> None:
        ...
    
    def _update_sprite(self, image: pygame.Surface) -> None:
        if self.angle_deg:
            pygame.transform.rotate(image, self.angle_deg)
        if self.scale != 1.0:
            size = (image.get_width() * self.scale, image.get_height() * self.scale)
            image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect(midbottom=self.pos)
        self.mask = pygame.mask.from_surface(self.image)


class Controls:
    def key_tap(self, key: int) -> None: ...
    def mouse_tap(self, button: int) -> None: ...
    def mouse_held(self, buttons: tuple[int]) -> None: ...
    def key_held(self, keys: pygame.key.ScancodeWrapper) -> None: ...


class Animation(Graphics, Controls):
    def __init__(self, config_id: str, asset_id: str, fps: int, reset_idx: bool=True) -> None:
        Graphics.__init__(self)
        self._reset_frame_idx()
        self.configs = {}
        self.config_id_fallback = config_id
        self._create_config(config_id, asset_id, fps, reset_idx)
        self._switch_config(config_id, is_fallback=True)
    
    def _reset_frame_idx(self) -> None:
        self.float_frame_idx = 0
        self.int_frame_idx = 0
        self.pre_frame_idx = 0
        self.current_frame_idx = 0
    
    def _create_config(self, config_id: str, asset_id: str, fps: int=14, reset_idx: bool=True, loops: int=-1) -> None:
        if not config_id:
            config_id = 'null'
        frames = get_gfx(asset_id, is_animation=True)
        asset_id = frames['asset_id']
        self.configs.update({
            config_id: {
            'frames': frames,
            'fps': fps,
            'reset_idx': reset_idx,
            'loops': loops
            }
        })
    
    def _switch_config(self, config_id: str, is_fallback: bool=False) -> None:
        if config_id not in self.configs:
            print(f'{colorama.Fore.RED}Failed to apply config.\nConfig ID: "{config_id}" not found!')
            return

        self.config_id = config_id
        self.current_config = self.configs[config_id] 
        self.frames = self.current_config['frames']
        self.asset_id = self.current_config['frames']['asset_id']
        self.total_frames = self.current_config['frames']['total_frames']
        self.is_animated = self.total_frames != 1

        if is_fallback:
            self.config_id_fallback = config_id

        if self.is_animated:
            self._handle_animation_config()
        else:
            self._reset_frame_idx()

        self._set_image()
        # print(f'Switched to {config_id} config; [animated: {self.is_animated}, fallback: {is_fallback}]')
    
    def _handle_animation_config(self) -> None:
        self.reset_idx = self.current_config['reset_idx']
        self.fps = self.current_config['fps']
        self.loops = self.current_config['loops']
        self.loop_count = 0
        if self.reset_idx:
            self._reset_frame_idx()
    
    def _update_frame(self, dt: float) -> None:
        if not self.is_animated:
            return

        self._update_frame_idx(dt)
        if self.current_frame_idx != self.pre_frame_idx:
            self.pre_frame_idx = self.int_frame_idx
            self._handle_loops()
            self._handle_keyframes()
            self._set_image()
            self._handle_fallback()

    def _update_frame_idx(self, dt: float) -> None:
        self.float_frame_idx = (self.float_frame_idx + self.fps * dt) % self.total_frames
        self.int_frame_idx = int(self.float_frame_idx)
        self.current_frame_idx = self.int_frame_idx
    
    def _handle_loops(self) -> None:
        if self.loops <= 0:
            return 
        if self.current_frame_idx % self.total_frames == 0:
            self.loop_count = self.loop_count + 1
    
    def _handle_keyframes(self) -> None: ...

    def _handle_fallback(self) -> None:
        if self.loops <= 0:
            return
        if self.loop_count == self.loops:
            self._switch_config(self.config_id_fallback, is_fallback=True)
    
    def _set_image(self) -> None:
        if image := self.frames.get(f'{self.asset_id}-{self.current_frame_idx}'):
            self._update_sprite(image)
    
    def _print_current_config(self) -> None:
        cfg = {} 
        cfg['frames'] = {}

        for key in self.current_config:
            if key == 'frames':
                continue
            value = str(self.current_config[key])
            cfg.update({key: value})

        for key in self.current_config['frames']:
            value = str(self.current_config['frames'][key])
            cfg['frames'].update({key: value})
        
        print(json.dumps(cfg, sort_keys=True, indent=4))


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
