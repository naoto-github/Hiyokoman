from __future__ import annotations
import numpy as np
import pyxel

from .base import Scene
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..renderer import blit, fill, scaled_text
from ..assets import Assets
from ..audio import AudioManager


class TransformScene(Scene):
    _DURATION = 30  # frames

    def __init__(
        self,
        scenes: "SceneManager",  # type: ignore[name-defined]
        from_type: int,
        to_type: int,
    ) -> None:
        super().__init__(scenes)
        self._tick = 0
        self._from = from_type
        self._to = to_type
        AudioManager.get().play_se("transform")

    def update(self) -> None:
        self._tick += 1
        if self._tick >= self._DURATION:
            self._scenes.pop()

    def draw(self, screen: np.ndarray) -> None:
        fill(screen, 0)
        assets = Assets.get()
        t = self._tick / self._DURATION
        # Fade from old to new type image
        htype = self._to if t > 0.5 else self._from
        if assets.hiyoko_big:
            px, mk = assets.hiyoko_big[htype]
            blit(screen, px, mk, SCREEN_WIDTH // 2 - 64, SCREEN_HEIGHT // 2 - 64)
        s = "TRANSFORM!"
        scaled_text(screen, SCREEN_WIDTH // 2 - len(s) * pyxel.FONT_WIDTH, SCREEN_HEIGHT // 2 + 72, s, 14)
