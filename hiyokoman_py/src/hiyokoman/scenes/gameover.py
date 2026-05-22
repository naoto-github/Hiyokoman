from __future__ import annotations
import numpy as np
import pyxel

from .base import Scene
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..renderer import blit, fill, scaled_text
from ..assets import Assets
from ..audio import AudioManager
from ..game_state import GameState


class GameOverScene(Scene):
    def __init__(
        self,
        scenes: "SceneManager",  # type: ignore[name-defined]
        htype: int,
    ) -> None:
        super().__init__(scenes)
        self._htype = htype
        self._stage = GameState.get().stage
        self._tick = 0
        AudioManager.get().stop_bgm()
        AudioManager.get().play_bgm("gameover", loops=0)

    def update(self) -> None:
        self._tick += 1
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            AudioManager.get().stop_bgm()
            GameState.get().score = 0
            from .battle import BattleScene
            self._scenes.replace(BattleScene(self._scenes, self._stage))

    def draw(self, screen: np.ndarray) -> None:
        fill(screen, 0)
        assets = Assets.get()
        if assets.hiyoko_big:
            px, mk = assets.hiyoko_big[self._htype]
            blit(screen, px, mk, SCREEN_WIDTH // 2 - 64, 80)
        s = "GAME OVER"
        scaled_text(screen, SCREEN_WIDTH // 2 - len(s) * pyxel.FONT_WIDTH, SCREEN_HEIGHT // 2 + 50, s, 12)
        s = f"SCORE: {GameState.get().score}"
        scaled_text(screen, SCREEN_WIDTH // 2 - len(s) * pyxel.FONT_WIDTH, SCREEN_HEIGHT // 2 + 64, s, 15)
        if (self._tick // 20) % 2 == 0:
            s = "SPACE: RETRY"
            scaled_text(screen, SCREEN_WIDTH // 2 - len(s) * pyxel.FONT_WIDTH, SCREEN_HEIGHT // 2 + 78, s, 15)
