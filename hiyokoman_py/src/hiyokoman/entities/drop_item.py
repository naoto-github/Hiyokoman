from __future__ import annotations
import numpy as np

from .base import Entity
from ..constants import APPLE, BANANA, GRAPES
from ..renderer import blit
from ..assets import Assets

_FRAME = {APPLE: 15, BANANA: 16, GRAPES: 17}


class DropItem(Entity):
    """Fruit dropped by a defeated monster — icon0.png tiles 15–17."""

    def __init__(self, x: float, y: float, itype: int) -> None:
        super().__init__(x, y, 16, 16)
        self.itype = itype
        self.radius = 12.0
        self.score = 10
        self.active = False
        self.visible = False

    def show(self) -> None:
        self.active = True
        self.visible = True

    def remove(self) -> None:
        self.active = False
        self.visible = False

    def draw(self, screen: np.ndarray) -> None:
        if not self.visible:
            return
        assets = Assets.get()
        if assets.icons is None:
            return
        px, mk = assets.icons.frame(_FRAME[self.itype])
        blit(screen, px, mk, int(self.x), int(self.y))
