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
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)


class Animation(Graphics):
    def __init__(self, asset_id: str, fps: int) -> None:
        Graphics.__init__(self)
        self._update_frames(asset_id, fps)
    
    def _update_frames(self, asset_id: str, fps: int, reset_idx: bool=True) -> None:
        self.frames = get_frames(asset_id)
        self.asset_id = self.frames['asset_id']
        self.total_frames = len(self.frames) - 1
        self.fps = fps
        if reset_idx:
            self.frame_idx_raw = 0
            self.pre_frame_idx = 0
            self.frame_idx = 0
        self._set_image()
    
    def _update_frame(self, dt: float) -> None:
        self.frame_idx_raw = (self.frame_idx_raw + self.fps * dt) % self.total_frames
        int_frame_idx = int(self.frame_idx_raw)
        self.frame_idx = int_frame_idx

        if self.frame_idx != self.pre_frame_idx:
            self.pre_frame_idx = int_frame_idx
            self._set_image()
    
    def _set_image(self) -> None:
        if image := self.frames.get(f'{self.asset_id}-{self.frame_idx}'):
            self._update_sprite(image)
