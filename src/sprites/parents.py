import pygame
import json
import colorama
from pygame.math import Vector2
from src.loader import get_gfx


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

        self._update_image()
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
            self._update_image()
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
    
    def update_scale(self, scale: float) -> None:
        self.scale = scale
        self._update_image()
    
    def _update_image(self) -> None:
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
