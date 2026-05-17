from __future__ import annotations
import math
import random
import numpy as np

from .base import Entity
from ..constants import (
    SLIME, BAT, WARM, ROCK, DRAGON, THUNDER, ORIGINAL,
    SCREEN_WIDTH, SCREEN_HEIGHT,
)
from ..renderer import blit
from ..assets import Assets


class Monster(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        hiyoko: "Hiyoko",  # type: ignore[name-defined]
        mtype: int,
        hmap: "HiyokoMap",  # type: ignore[name-defined]
    ) -> None:
        cfg = _CONFIG[mtype]
        super().__init__(x, y, cfg["w"], cfg["h"])
        self.mtype = mtype
        self.hiyoko = hiyoko
        self.map = hmap
        self.life: int = cfg["life"]
        self.attack_power: int = cfg["attack"]
        self.speed: float = cfg["speed"]
        self.radius: float = cfg["radius"]
        self.drop_rate: float = cfg["rate"]
        self.score_value: int = cfg["score"]
        self.frame: int = cfg["frame"]
        self.tick = 0
        self.counter = 0
        self._attack_flg = False
        self._attack_frq: int = cfg.get("attack_frq", 200)
        self._attack_rnd: int = random.randint(0, self._attack_frq - 1)

        # THUNDER: position adjusted toward hiyoko
        if mtype == THUNDER:
            angle = math.atan2(
                (hiyoko.cx - x), (hiyoko.cy - y)
            )
            r = 64
            self.x = x - self.width / 2 + r * math.sin(angle)
            self.y = y + r * math.cos(angle) - self.height

        # ROCK: compute direction once
        if mtype == ROCK:
            self._angle = math.atan2(hiyoko.cx - x, hiyoko.cy - y)

    @property
    def alive(self) -> bool:
        return self.life > 0

    def is_hit(self, hiyoko: "Hiyoko") -> bool:  # type: ignore[name-defined]
        if self.mtype == THUNDER:
            return self.intersect(hiyoko)
        return self.within(hiyoko, self.radius)

    def action(self) -> "Monster | None":
        """Update monster state. Returns a new spawned projectile or None."""
        result = None

        if self.mtype in (SLIME, BAT, ORIGINAL):
            if self.alive:
                self.frame = (self.tick % 4) + 2
                self._move_toward_hiyoko()
            else:
                self._die_anim()

        elif self.mtype == WARM:
            if self.alive:
                if not self._attack_flg:
                    if random.random() < 0.01:
                        self._attack_flg = True
                else:
                    if self.frame == 10:
                        self.frame = 6
                        self._attack_flg = False
                        result = Monster(
                            self.cx, self.cy, self.hiyoko, ROCK, self.map
                        )
                    else:
                        self.frame += 1
            else:
                self._die_anim()

        elif self.mtype == DRAGON:
            if self.alive:
                if not self._attack_flg:
                    if self.tick % self._attack_frq == self._attack_rnd:
                        self._attack_flg = True
                else:
                    if self.frame == 10:
                        self.frame = 6
                        self._attack_flg = False
                        result = Monster(
                            self.cx, self.cy, self.hiyoko, THUNDER, self.map
                        )
                        from ..audio import AudioManager
                        AudioManager.get().play_se("thunder")
                    else:
                        self.frame += 1
            else:
                self._die_anim()

        elif self.mtype == ROCK:
            if self.alive:
                self.x += self.speed * math.sin(self._angle)
                self.y += self.speed * math.cos(self._angle)
                if (
                    self.x > SCREEN_WIDTH
                    or self.y > SCREEN_HEIGHT
                    or self.x < -self.width
                    or self.y < -self.height
                ):
                    self.visible = False
            else:
                self._die_anim()

        elif self.mtype == THUNDER:
            if self.alive:
                if self.frame >= 7:
                    self.visible = False
                else:
                    self.frame += 1
            else:
                self._die_anim()

        self.tick += 1
        return result

    def _die_anim(self) -> None:
        if self.counter == 5:
            self.visible = False
            from ..game_state import GameState
            GameState.get().score += self.score_value
        else:
            self.frame = self.counter
        self.counter += 1

    def _move_toward_hiyoko(self) -> None:
        dx = self.hiyoko.cx - self.cx
        dy = self.hiyoko.cy - self.cy
        moved_x = self._step_x(1 if dx >= 0 else -1)
        if moved_x:
            self._step_y(1 if dy >= 0 else -1)

    def _step_x(self, sign: int) -> bool:
        self.x += self.speed * sign
        if self._collides():
            self.x -= self.speed * sign
            return False
        return True

    def _step_y(self, sign: int) -> None:
        self.y += self.speed * sign
        if self._collides():
            self.y -= self.speed * sign

    def _collides(self) -> bool:
        if self.mtype == SLIME:
            return self.map.is_hit(self.cx, self.cy)
        return False  # BAT, ORIGINAL, WARM fly over terrain

    def drop(self) -> "DropItem | None":  # type: ignore[name-defined]
        from .drop_item import DropItem
        from ..constants import APPLE, BANANA, GRAPES

        if random.random() >= self.drop_rate:
            return None
        itype = random.randint(0, 2)
        item = DropItem(self.cx, self.cy, itype)
        item.x -= item.width / 2
        item.y -= item.height / 2
        return item

    def draw(self, screen: np.ndarray) -> None:
        if not self.visible:
            return
        assets = Assets.get()

        if not self.alive and self.mtype not in (ROCK, THUNDER):
            # Death effect
            if assets.effect:
                px, mk = assets.effect.frame(min(self.counter, 4))
                blit(screen, px, mk, int(self.x), int(self.y))
            return

        if self.mtype == ROCK:
            px, mk = assets.monster_map0_rock
        elif self.mtype == THUNDER:
            px, mk = assets.monster_thunder.frame(min(self.frame, 7))
        else:
            sheet = assets.monster.get(self.mtype)
            if sheet is None:
                return
            px, mk = sheet.frame(self.frame)

        blit(screen, px, mk, int(self.x), int(self.y))


_CONFIG: dict[int, dict] = {
    SLIME:    {"w": 48, "h": 48, "life": 5,    "attack": 1, "speed": 1.0, "radius": 10.0, "rate": 0.1, "score": 10,  "frame": 2},
    BAT:      {"w": 48, "h": 48, "life": 5,    "attack": 1, "speed": 1.2, "radius": 10.0, "rate": 0.1, "score": 20,  "frame": 2},
    WARM:     {"w": 80, "h": 80, "life": 100,  "attack": 1, "speed": 0.0, "radius": 16.0, "rate": 0.1, "score": 50,  "frame": 6},
    ROCK:     {"w": 16, "h": 16, "life": 9999, "attack": 1, "speed": 4.0, "radius": 8.0,  "rate": 0.0, "score": 0,   "frame": 27},
    DRAGON:   {"w": 80, "h": 80, "life": 200,  "attack": 1, "speed": 0.0, "radius": 16.0, "rate": 0.1, "score": 100, "frame": 6, "attack_frq": 200},
    THUNDER:  {"w": 64, "h": 240,"life": 9999, "attack": 1, "speed": 0.0, "radius": 32.0, "rate": 0.0, "score": 0,   "frame": 0},
    ORIGINAL: {"w": 32, "h": 32, "life": 5,    "attack": 1, "speed": 1.0, "radius": 10.0, "rate": 0.1, "score": 10,  "frame": 0},
}
