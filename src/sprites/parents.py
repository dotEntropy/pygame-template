import pygame
import json
from pygame.math import Vector2
from src.loader import get_frames
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


class Animation(Graphics):
    def __init__(self, config_id: str, asset_id: str, fps: int) -> None:
        Graphics.__init__(self)
        self.configs = {}
        self.config_id_fallback = config_id
        self._create_config(config_id, asset_id, fps)
        self._switch_config(config_id)
    
    def _create_config(self, config_id: str, asset_id: str, fps: int, reset_idx: bool=True, loop: bool=True) -> None:
        frames = get_frames(asset_id)
        asset_id = frames['asset_id']
        self.configs.update({
            config_id: {
            'frames': frames,
            'total_frames': len(frames) - 1,
            'fps': fps,
            'reset_idx': reset_idx,
            'loop': loop
            }
        })
    
    def _switch_config(self, config_id: str, is_fallback: bool=False) -> None:
        if config_id not in self.configs:
            print(f'Config ID "{config_id}" does not exist!')
            return
        self.config_id = config_id
        self.current_config = self.configs[config_id] 
        self.asset_id = self.current_config['frames']['asset_id']
        self.frames = self.current_config['frames']
        self.total_frames = self.current_config['total_frames']
        self.fps = self.current_config['fps']
        self.reset_idx = self.current_config['reset_idx']
        self.loop = self.current_config['loop']

        if self.reset_idx:
            self.float_frame_idx = 0
            self.int_frame_idx = 0
            self.pre_frame_idx = 0
            self.current_frame_idx = 0

        if self.loop:
            self.config_id_fallback = config_id
        
        if not is_fallback:
            self._handle_keyframes()
        self._set_image()
    
    def _update_frame(self, dt: float) -> None:
        self._update_frame_idx(dt)
        if self.current_frame_idx != self.pre_frame_idx:
            self.pre_frame_idx = self.int_frame_idx
            self._handle_fallback()
            self._handle_keyframes()
            self._set_image()
    
    def _update_frame_idx(self, dt: float) -> None:
        self.float_frame_idx = (self.float_frame_idx + self.fps * dt) % self.total_frames
        self.int_frame_idx = int(self.float_frame_idx)
        self.current_frame_idx = self.int_frame_idx
    
    
    def _handle_fallback(self) -> None:
        if not self.loop and self.current_frame_idx % self.total_frames == 0:
            self._switch_config(self.config_id_fallback, is_fallback=True)
        
    def _handle_keyframes(self) -> None:
        ...
    
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
