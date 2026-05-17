from __future__ import annotations
import numpy as np

from .base import Entity
from ..renderer import blit
from ..assets import Assets


class Key(Entity):
    """Collectible key — icon0.png tile #33."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 16, 16)
        self.radius = 12.0
        self.active = True

    def remove(self) -> None:
        self.active = False
        self.visible = False

    def draw(self, screen: np.ndarray) -> None:
        if not self.visible:
            return
        assets = Assets.get()
        if assets.icons is None:
            return
        px, mk = assets.icons.frame(33)
        blit(screen, px, mk, int(self.x), int(self.y))
