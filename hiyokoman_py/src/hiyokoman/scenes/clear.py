from __future__ import annotations
import numpy as np
import pyxel

from .base import Scene
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..renderer import blit, fill
from ..assets import Assets
from ..audio import AudioManager
from ..game_state import GameState


class ClearScene(Scene):
    def __init__(
        self,
        scenes: "SceneManager",  # type: ignore[name-defined]
        htype: int,
        time_left: int,
    ) -> None:
        super().__init__(scenes)
        self._htype = htype
        self._time_left = time_left
        self._tick = 0
        AudioManager.get().stop_bgm()
        AudioManager.get().play_bgm("clear")
        state = GameState.get()
        state.score += time_left * 10
        self._score = state.score

    def update(self) -> None:
        self._tick += 1
        state = GameState.get()
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            AudioManager.get().stop_bgm()
            next_stage = state.stage + 1
            if next_stage <= 4:
                state.stage = next_stage
                from .battle import BattleScene
                self._scenes.replace(BattleScene(self._scenes, next_stage))
            else:
                # All stages cleared — return to opening
                state.reset()
                from .opening import OpeningScene
                self._scenes.replace(OpeningScene(self._scenes))

    def draw(self, screen: np.ndarray) -> None:
        fill(screen, 4)
        assets = Assets.get()
        if assets.hiyoko_big:
            px, mk = assets.hiyoko_big[self._htype]
            blit(screen, px, mk, SCREEN_WIDTH // 2 - 64, 30)
        pyxel.text(SCREEN_WIDTH // 2 - 12, SCREEN_HEIGHT // 2 + 50, "CLEAR!", 14)
        pyxel.text(SCREEN_WIDTH // 2 - 28, SCREEN_HEIGHT // 2 + 62,
                   f"SCORE: {self._score}", 15)
        if (self._tick // 20) % 2 == 0:
            pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 76,
                       "SPACE: CONTINUE", 15)
