from __future__ import annotations
import math
import numpy as np
import pyxel

from .base import Entity
from .hiyoko_map import HiyokoMap
from ..constants import YELLOW, RED, BLUE, DAGGER, SWORD, ROD, SCREEN_WIDTH, SCREEN_HEIGHT
from ..renderer import blit
from ..assets import Assets


class Hiyoko(Entity):
    def __init__(self, x: float, y: float, htype: int, hmap: HiyokoMap) -> None:
        super().__init__(x, y, 32, 32)
        self.map = hmap
        self.tick = 0
        self.weapon_type = DAGGER
        self.life = 1
        self.key_count = 0
        self.counter = 0
        self.frame = 7
        self.speed = 4.0
        self._dead_callback: "callable | None" = None
        self.change(htype)

    @property
    def htype(self) -> int:
        return self._htype

    def change(self, htype: int) -> None:
        self._htype = htype
        if htype == YELLOW:
            self.weapon_type = DAGGER
            self.speed = 4.0
        elif htype == RED:
            self.weapon_type = ROD
            self.speed = 2.0
        elif htype == BLUE:
            self.weapon_type = SWORD
            self.speed = 3.0

    @property
    def alive(self) -> bool:
        return self.life > 0

    def on_death(self, callback: "callable") -> None:
        self._dead_callback = callback

    def update(self) -> None:
        if self.alive:
            self._move()
        else:
            self.counter += 1
            if self.counter == 6 and self._dead_callback:
                self._dead_callback()
        self.tick += 1

    def _move(self) -> None:
        moved = False
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self._move_x(-self.speed)
            self.frame = (self.tick % 3) + 12
            moved = True
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self._move_x(self.speed)
            self.frame = (self.tick % 3) + 15
            moved = True
        elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self._move_y(-self.speed)
            self.frame = (self.tick % 3) + 9
            moved = True
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self._move_y(self.speed)
            self.frame = (self.tick % 3) + 6
            moved = True

    def _move_x(self, dx: float) -> None:
        self.x += dx
        if self.map.is_hit(self.cx, self.cy):
            self.x -= dx

    def _move_y(self, dy: float) -> None:
        self.y += dy
        if self.map.is_hit(self.cx, self.cy):
            self.y -= dy

    def attack(self) -> "Weapon":  # type: ignore[name-defined]
        from .weapon import Weapon

        if self.frame in (12, 13, 14):
            angle = math.pi * 1.5
        elif self.frame in (15, 16, 17):
            angle = math.pi * 0.5
        elif self.frame in (9, 10, 11):
            angle = math.pi
        else:
            angle = 0.0
        return Weapon(self.cx, self.cy, self, self.weapon_type, angle, self.map)

    def draw(self, screen: np.ndarray) -> None:
        assets = Assets.get()
        sheet = assets.hiyoko[self._htype]
        if self.alive:
            px, mk = sheet.frame(self.frame)
        else:
            f = min(self.counter + 3, 5)
            px, mk = sheet.frame(f)
        blit(screen, px, mk, int(self.x), int(self.y))
