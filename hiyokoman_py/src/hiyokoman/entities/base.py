from __future__ import annotations
import math


class Entity:
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True

    @property
    def cx(self) -> float:
        return self.x + self.width / 2

    @property
    def cy(self) -> float:
        return self.y + self.height / 2

    def within(self, other: "Entity", radius: float) -> bool:
        dx = self.cx - other.cx
        dy = self.cy - other.cy
        return dx * dx + dy * dy <= radius * radius

    def intersect(self, other: "Entity") -> bool:
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )
