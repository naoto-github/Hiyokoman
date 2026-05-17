from __future__ import annotations
import math
import numpy as np

from .base import Entity
from ..constants import DAGGER, SWORD, ROD, SCREEN_WIDTH, SCREEN_HEIGHT
from ..renderer import blit
from ..assets import Assets


class Weapon(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        hiyoko: "Hiyoko",  # type: ignore[name-defined]
        wtype: int,
        angle: float,
        hmap: "HiyokoMap",  # type: ignore[name-defined]
    ) -> None:
        if wtype == DAGGER:
            super().__init__(x - 23, y - 23, 46, 46)
            self.damage = 5
            self.radius = 12.0
            self._speed = 5.0
        elif wtype == SWORD:
            super().__init__(x - 48, y - 48, 96, 96)
            self.damage = 10
            self.radius = 24.0
            self._speed = 0.0
        else:  # ROD
            super().__init__(
                x - 48 + math.sin(angle) * 48,
                y - 48 + math.cos(angle) * 48,
                96, 96,
            )
            self.damage = 1
            self.radius = 48.0
            self._speed = 0.0

        self.wtype = wtype
        self.angle = angle
        self.hiyoko = hiyoko
        self.map = hmap
        self.frame = 0
        self.tick = 0

        # Rotation angle for DAGGER sprite (degrees, CCW)
        self._rot_deg = (-angle * 180.0 / math.pi) % 360

    @property
    def active(self) -> bool:
        return self.damage != 0 and self.visible

    def remove(self) -> None:
        self.damage = 0
        self.visible = False

    def attack(self, monster: "Monster") -> None:  # type: ignore[name-defined]
        monster.life -= self.damage
        if self.wtype == DAGGER:
            self.remove()

    def update(self) -> None:
        if not self.active:
            self.visible = False
            return

        if self.wtype == DAGGER:
            self.x += self._speed * math.sin(self.angle)
            self.y += self._speed * math.cos(self.angle)
            out = (
                self.x > SCREEN_WIDTH
                or self.y > SCREEN_HEIGHT
                or self.x < -self.width
                or self.y < -self.height
            )
            if out or self.map.is_hit(self.cx, self.cy):
                self.remove()
        elif self.wtype == SWORD:
            self.x = self.hiyoko.cx - self.width / 2
            self.y = self.hiyoko.cy - self.height / 2
            if self.frame >= 10:
                self.remove()
            else:
                self.frame += 1
        else:  # ROD
            if self.frame >= 8:
                self.remove()
            else:
                self.frame += 1

        self.tick += 1

    def draw(self, screen: np.ndarray) -> None:
        if not self.visible:
            return
        assets = Assets.get()
        sheet = assets.weapon[self.wtype]
        if self.wtype == DAGGER:
            px, mk = sheet.rotated_frame(0, self._rot_deg)
        else:
            px, mk = sheet.frame(self.frame)
        blit(screen, px, mk, int(self.x), int(self.y))
