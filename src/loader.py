import pygame
import pathlib
import os
from src.variables import GameVars
from src.constants import *
from utils.console import print_success


class AssetLoader:
    def __init__(self) -> None:
        self.ASSET_DIR = pathlib.Path(__file__).parent.parent / 'assets' 
        self.gfx_cache = {}
        self.sfx_cache = {}
        self.load_assets('gfx', ('png', 'jpg'), self.load_image)
        self.load_assets('sfx', ('mp3', 'wav', 'ogg'), pygame.mixer.Sound)
        print_success(f'Frames Loaded: {list(self.gfx_cache.keys())}')
        print_success(f'SFX Loaded: {list(self.sfx_cache.keys())}')

    def load_assets(self, folder_name: str, ext_names: tuple[str], loader: object) -> None:
        for file in os.listdir(self.ASSET_DIR / folder_name):
            name = self.strip_ext(file, ext_names)
            asset = loader(self.ASSET_DIR / folder_name / file)
            if folder_name == 'gfx':
                self.load_frames(name, asset)
            if folder_name == 'sfx':
                self.sfx_cache.update({name: asset})

    def strip_ext(self, file: str, ext_names: tuple[str]) -> str:
        for ext_name in ext_names:
            if file.endswith(f'.{ext_name}'):
                file = file.removesuffix(f'.{ext_name}')
                return file
    
    def load_frames(self, name: str, asset: pygame.Surface) -> None:
        if not name[-1].isdigit():
            return
        asset_id = name[:name.rfind('-')]
        if asset_id not in self.gfx_cache:
            self.gfx_cache.update({asset_id: {}})
        self.gfx_cache[asset_id].update({name: asset})
    
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


def get_gfx(asset_id: str, is_animation: bool=False) -> dict[str: pygame.Surface]:
    cache = asset.gfx_cache
    if asset_id not in cache:
        asset_id = 'default'
    frames = cache.get(asset_id).copy()
    total_frames = len(frames)
    frames.update({'asset_id': asset_id})
    frames.update({'total_frames': total_frames})
    if not is_animation:
        return list(frames.values())[0]
    return frames


def get_sfx(asset_id: str) -> pygame.mixer.Sound:
    cache = asset.sfx_cache
    sfx = cache.get(asset_id, cache['default'])
    return sfx


def get_font(asset_id: str, size: int=20) -> pygame.font.Font:
    font = pygame.font.Font(asset.ASSET_DIR / 'fonts' / f'{asset_id}.ttf', size)
    return font
