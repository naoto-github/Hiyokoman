from __future__ import annotations
import numpy as np


class Scene:
    def __init__(self, scenes: "SceneManager") -> None:  # type: ignore[name-defined]
        self._scenes = scenes

    def update(self) -> None: ...
    def draw(self, screen: np.ndarray) -> None: ...
