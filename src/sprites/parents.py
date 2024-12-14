import pygame
from src.loader import get_frames
from src.variables import GameVars


class Graphics:
    def __init__(self) -> None:
        pass
    
    def _update_sprite(self, image: pygame.Surface, scale: float=1.0, angle_deg: float=0) -> None:
        if angle_deg:
            pygame.transform.rotate(image, angle_deg)
        if scale != 1.0:
            size = (image.get_width() * scale, image.get_height() * scale)
            image = pygame.transform.scale(image, size)
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)


class Animation(Graphics):
    def __init__(self, asset_id: str, fps: int | float=1) -> None:
        self.asset_id = asset_id
        self.fps = fps
        self.frames = get_frames(asset_id)
        self.total_frames = len(self.frames)
        self.frame_idx_raw = 0
        self.pre_frame_idx = 0
        self.frame_idx = 0
        self._update_image(scale=3)
    
    def _update_frame(self, dt: float, scale: float=1.0, angle_deg: float=0) -> None:
        self.frame_idx_raw = (self.frame_idx_raw + self.fps * dt) % self.total_frames
        int_frame_idx = int(self.frame_idx_raw)
        self.frame_idx = int_frame_idx
        if self.frame_idx != self.pre_frame_idx:
            self.pre_frame_idx = int_frame_idx
            self._update_image(scale, angle_deg)
    
    def _update_image(self, scale: float=1.0, angle_deg: float=0) -> None:
        image = self.frames.get(f'{self.asset_id}-{self.frame_idx}')
        if image:
            self._update_sprite(image, scale, angle_deg)
