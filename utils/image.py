import pygame
from pygame.math import Vector2
from src.variables import GameVars


def scale(image: pygame.Surface, scale: float) -> pygame.Surface:
    scale_w = image.get_width() * scale
    scale_h = image.get_height() * scale
    image = pygame.transform.scale(image, (scale_w, scale_h))
    return image


def update_sprite_scale() -> None:
    w_ratio = GameVars.client_w / GameVars.GAME_W
    print(GameVars.client_w, GameVars.GAME_W)
    h_ratio = GameVars.client_h / GameVars.GAME_H
    GameVars.sprite_scale = Vector2(w_ratio, h_ratio)
