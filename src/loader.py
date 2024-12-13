import pygame
import pathlib
import os
from src.variables import GameVars
from src.constants import *
from utils.colored_print import print_success


class AssetLoader:
    def __init__(self) -> None:
        self.ASSET_DIR = pathlib.Path(__file__).parent.parent / 'assets' 
        self.gfx_cache = {}
        self.sfx_cache = {}
        self.font_cache = {}
        self.load_assets('gfx', ('png', 'jpg'), self.load_image)
        self.load_assets('sfx', ('mp3', 'wav', 'ogg'), pygame.mixer.Sound)
        print_success(f'GFX Loaded: {self.gfx_cache}')
        print_success(f'SFX Loaded: {self.sfx_cache}')

    def load_assets(self, folder_name: str, ext_names: tuple[str], loader: object) -> None:
        for file in os.listdir(self.ASSET_DIR / folder_name):
            name = self.verify_ext(file, ext_names)
            asset = {name: loader(self.ASSET_DIR / folder_name / file)}
            if folder_name == "gfx":
                self.gfx_cache.update(asset)
            if folder_name == "sfx":
                self.sfx_cache.update(asset)

    def verify_ext(self, file: str, ext_names: tuple[str]) -> str:
        for ext_name in ext_names:
            if file.endswith(f'.{ext_name}'):
                file = file.removesuffix(f'.{ext_name}')
                return file
    
    @staticmethod
    def load_image(path: str) -> pygame.Surface:
        image = pygame.image.load(path).convert_alpha()
        return image

pygame.init()
pygame.display.set_mode([DEFAULT_WIDTH, DEFAULT_HEIGHT])
display_info = pygame.display.Info()
GameVars.client_w = display_info.current_w
GameVars.client_h = display_info.current_h
asset = AssetLoader()


def get_gfx(asset_id: str) -> pygame.Surface:
    cache = asset.gfx_cache
    gfx = cache.get(asset_id, cache['default'])
    return gfx


def get_sfx(asset_id: str) -> pygame.mixer.Sound:
    cache = asset.sfx_cache
    sfx = cache.get(asset_id, cache['default'])
    return sfx


def get_font(asset_id: str, size: int=20) -> pygame.font.Font:
    font = pygame.font.Font(asset.ASSET_DIR / 'fonts' / f'{asset_id}.ttf', size)
    return font
