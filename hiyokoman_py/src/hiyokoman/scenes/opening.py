from __future__ import annotations
import numpy as np
import pyxel

from .base import Scene
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW
from ..renderer import blit, scaled_text
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
        # Background: bank 0 = left 256px, bank 1 = right 224px
        pyxel.blt(0,   0, 0, 0, 0, 256, 256)
        pyxel.blt(256, 0, 1, 0, 0, 224, 256)
        pyxel.rect(0, 256, 480, 64, 4)   # bottom strip (green)

        # Big hiyoko character
        assets = Assets.get()
        if assets.hiyoko_big:
            px, mk = assets.hiyoko_big[YELLOW]
            blit(screen, px, mk, SCREEN_WIDTH // 2 - 64, 80)

        if (self._tick // 15) % 2 == 0:
            s = "SPACE: START"
            scaled_text(screen, SCREEN_WIDTH // 2 - len(s) * pyxel.FONT_WIDTH, SCREEN_HEIGHT // 2 + 60, s, 15)
