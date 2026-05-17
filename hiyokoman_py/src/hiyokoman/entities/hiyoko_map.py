from __future__ import annotations
from ..constants import TILE_SIZE
from .. import map_data


class HiyokoMap:
    def __init__(self, stage: int) -> None:
        self.stage = stage
        self._collision = map_data.COLLISION[stage]
        self._rows = len(self._collision)
        self._cols = len(self._collision[0])

    def is_hit(self, x: float, y: float) -> bool:
        col = int(x // TILE_SIZE)
        row = int(y // TILE_SIZE)
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return True
        return bool(self._collision[row][col])
