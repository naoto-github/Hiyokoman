class GameState:
    _instance: "GameState | None" = None

    def __init__(self) -> None:
        self.stage: int = 1
        self.score: int = 0
        self.original: bool = False
        self.invincible: bool = False

    @classmethod
    def get(cls) -> "GameState":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reset(self) -> None:
        self.stage = 1
        self.score = 0
