from __future__ import annotations
import numpy as np

from .base import Entity
from ..renderer import blit
from ..assets import Assets


class Castle(Entity):
    """Goal — map0.png tile #20, hidden until all keys collected."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 16, 16)
        self.radius = 12.0
        self.visible = False

    def show(self) -> None:
        self.visible = True

    def draw(self, screen: np.ndarray) -> None:
        if not self.visible:
            return
        assets = Assets.get()
        sheet = assets.map_tiles.get("map0")
        if sheet is None:
            return
        px, mk = sheet.frame(20)
        blit(screen, px, mk, int(self.x), int(self.y))
