from __future__ import annotations
import random
import numpy as np

from .base import Entity
from .monster import Monster
from ..renderer import blit
from ..assets import Assets


class Nest(Entity):
    """Monster spawner — 16×16 sprite at map0 tile #22."""

    def __init__(
        self,
        x: float,
        y: float,
        hiyoko: "Hiyoko",  # type: ignore[name-defined]
        mtype: int,
        rate: float,
        hmap: "HiyokoMap",  # type: ignore[name-defined]
    ) -> None:
        super().__init__(x, y, 16, 16)
        self.hiyoko = hiyoko
        self.mtype = mtype
        self.rate = rate
        self.map = hmap

    def born(self) -> Monster | None:
        if random.random() >= self.rate:
            return None
        m = Monster(self.x, self.y, self.hiyoko, self.mtype, self.map)
        m.x = self.x - (m.width * 0.5)
        m.y = self.y - (m.height * 0.5)
        return m

    def draw(self, screen: np.ndarray) -> None:
        assets = Assets.get()
        sheet = assets.map_tiles.get("map0")
        if sheet is None:
            return
        px, mk = sheet.frame(22)
        blit(screen, px, mk, int(self.x), int(self.y))
