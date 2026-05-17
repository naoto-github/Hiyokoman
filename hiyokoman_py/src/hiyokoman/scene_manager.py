from __future__ import annotations
import numpy as np


class SceneManager:
    def __init__(self) -> None:
        self._stack: list["Scene"] = []  # type: ignore[name-defined]

    def push(self, scene: "Scene") -> None:  # type: ignore[name-defined]
        self._stack.append(scene)

    def pop(self) -> None:
        if self._stack:
            self._stack.pop()

    def replace(self, scene: "Scene") -> None:  # type: ignore[name-defined]
        self.pop()
        self.push(scene)

    def update(self) -> None:
        if self._stack:
            self._stack[-1].update()

    def draw(self, screen: np.ndarray) -> None:
        if self._stack:
            self._stack[-1].draw(screen)
