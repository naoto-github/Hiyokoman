from __future__ import annotations
import ctypes
import numpy as np
import pyxel

from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, DISPLAY_SCALE
from .game_state import GameState
from .assets import Assets
from .audio import AudioManager
from .renderer import setup_palette
from .scene_manager import SceneManager
from .scenes.opening import OpeningScene
from . import map_data


class Game:
    def __init__(self) -> None:
        pyxel.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="ひよこマン",
            fps=FPS,
            display_scale=DISPLAY_SCALE,
        )
        setup_palette()

        # Load assets (quantizes images at startup — takes a few seconds)
        print("Loading assets...")
        assets = Assets.get()
        assets.load(map_data)

        # Initialize audio
        AudioManager.get().init()

        # Start scene stack
        self._scenes = SceneManager()
        self._scenes.push(OpeningScene(self._scenes))
        print("Starting game.")

        pyxel.run(self._update, self._draw)

    def _update(self) -> None:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        ctrl = pyxel.btn(pyxel.KEY_LCTRL) or pyxel.btn(pyxel.KEY_RCTRL)
        if ctrl:
            from .scenes.battle import BattleScene
            for stage, key in ((1, pyxel.KEY_1), (2, pyxel.KEY_2), (3, pyxel.KEY_3), (4, pyxel.KEY_4)):
                if pyxel.btnp(key):
                    AudioManager.get().stop_bgm()
                    self._scenes.reset(BattleScene(self._scenes, stage))
                    return

        self._scenes.update()

    def _draw(self) -> None:
        pyxel.cls(0)
        # Build a numpy view of Pyxel's screen pixel buffer (palette indices)
        ptr = pyxel.screen.data_ptr()
        screen = np.frombuffer(ptr, dtype=np.uint8).reshape(
            (SCREEN_HEIGHT, SCREEN_WIDTH)
        )
        self._scenes.draw(screen)


def main() -> None:
    Game()


if __name__ == "__main__":
    main()
