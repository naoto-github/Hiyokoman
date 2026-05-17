from __future__ import annotations
import numpy as np
import pyxel

from .base import Scene
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW
from ..renderer import blit, fill
from ..assets import Assets
from ..audio import AudioManager
from ..game_state import GameState


class OpeningScene(Scene):
    def __init__(self, scenes: "SceneManager") -> None:  # type: ignore[name-defined]
        super().__init__(scenes)
        self._tick = 0
        AudioManager.get().play_bgm("opening")

    def update(self) -> None:
        self._tick += 1
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            from .battle import BattleScene
            AudioManager.get().stop_bgm()
            AudioManager.get().play_se("select")
            GameState.get().reset()
            self._scenes.replace(BattleScene(self._scenes, 1))

    def draw(self, screen: np.ndarray) -> None:
        fill(screen, 4)  # green background

        # Big hiyoko character
        assets = Assets.get()
        if assets.hiyoko_big:
            px, mk = assets.hiyoko_big[YELLOW]
            blit(screen, px, mk, SCREEN_WIDTH // 2 - 64, 40)

        # Blinking start text
        if (self._tick // 15) % 2 == 0:
            pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 60, "SPACE: START", 15)

        pyxel.text(4, 4, "HIYOKOMAN", 15)
