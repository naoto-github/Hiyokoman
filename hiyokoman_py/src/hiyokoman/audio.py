from __future__ import annotations
from pathlib import Path

from .constants import ASSET_ROOT


class AudioManager:
    _instance: "AudioManager | None" = None

    def __init__(self) -> None:
        self._ok = False
        self._bgm_channel: "pygame.mixer.Channel | None" = None  # type: ignore[name-defined]
        self._bgm_sound: "pygame.mixer.Sound | None" = None      # type: ignore[name-defined]
        self._sounds: dict[str, "pygame.mixer.Sound"] = {}       # type: ignore[name-defined]

    @classmethod
    def get(cls) -> "AudioManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def init(self) -> None:
        try:
            import pygame.mixer as mx
            mx.pre_init(44100, -16, 2, 1024)
            mx.init()
            self._mx = mx
            self._ok = True
            self._load_all()
        except Exception as e:
            print(f"[audio] pygame.mixer unavailable: {e}")

    def _load_all(self) -> None:
        root = ASSET_ROOT / "sound"
        files = {
            "opening":    "opening_bgm.mp3",
            "stage1":     "firstmap_bgm.mp3",
            "stage2":     "secondmap_bgm.mp3",
            "stage3":     "thirdmap_bgm.mp3",
            "stage4":     "finalmap_bgm.mp3",
            "gameover":   "gameover_bgm.mp3",
            "clear":      "clear_bgm.mp3",
            "select":     "select.wav",
            "attack_dagger": "attack_dagger.wav",
            "attack_sword":  "attack_sword.mp3",
            "attack_rod":    "attack_rod.mp3",
            "bomb":       "bomb.mp3",
            "get":        "get.wav",
            "castle":     "castle.wav",
            "clash":      "clash.mp3",
            "transform":  "transform.mp3",
            "thunder":    "thunder.mp3",
        }
        for key, fname in files.items():
            p = root / fname
            if p.exists():
                try:
                    self._sounds[key] = self._mx.Sound(str(p))
                except Exception:
                    pass

        self._bgm_channel = self._mx.Channel(0)

    def play_bgm(self, key: str) -> None:
        if not self._ok or key not in self._sounds:
            return
        snd = self._sounds[key]
        if self._bgm_channel:
            self._bgm_channel.stop()
            self._bgm_channel.play(snd, loops=-1)

    def stop_bgm(self) -> None:
        if self._ok and self._bgm_channel:
            self._bgm_channel.stop()

    def play_se(self, key: str) -> None:
        if not self._ok or key not in self._sounds:
            return
        self._sounds[key].play()

    def bgm_key_for_stage(self, stage: int) -> str:
        return f"stage{stage}"
