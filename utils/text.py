import pygame
from pygame.math import Vector2
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
