import pygame
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
        self._update_config(config_id, asset_id, fps)
        self._switch_config(config_id)
    
    def _update_config(self, config_id: str, asset_id: str, fps: int, reset_idx: bool=True, loop: bool=True) -> None:
        frames = get_frames(asset_id)
        asset_id = frames['asset_id']
        self.configs.update({
            config_id: {
            'asset_id': asset_id,
            'frames': frames,
            'total_frames': len(frames) - 1,
            'fps': fps,
            'reset_idx': reset_idx,
            'loop': loop
            }
            })
    
    def _switch_config(self, config_id: str) -> None:
        if config_id not in self.configs:
            print(f'Config ID "{config_id}" does not exist!')
            return
        config = self.configs[config_id] 
        self.asset_id = config['asset_id']
        self.frames = config['frames']
        self.total_frames = config['total_frames']
        self.fps = config['fps']
        self.reset_idx = config['reset_idx']
        self.loop = config['loop']

        if self.reset_idx:
            self.frame_idx_raw = 0
            self.pre_frame_idx = 0
            self.frame_idx = 0

        if self.loop:
            self.config_id_fallback = config_id

        self._set_image()
    
    def _update_frame(self, dt: float) -> None:
        self.frame_idx_raw = (self.frame_idx_raw + self.fps * dt) % self.total_frames
        int_frame_idx = int(self.frame_idx_raw)
        self.frame_idx = int_frame_idx

        if self.frame_idx != self.pre_frame_idx:
            self.pre_frame_idx = int_frame_idx
            self._handle_single_loop()
            self._set_image() 
    
    def _handle_single_loop(self) -> None:
        if not self.loop and self.frame_idx % self.total_frames == 0:
            self._switch_config(self.config_id_fallback)
    
    def _set_image(self) -> None:
        if image := self.frames.get(f'{self.asset_id}-{self.frame_idx}'):
            self._update_sprite(image)
