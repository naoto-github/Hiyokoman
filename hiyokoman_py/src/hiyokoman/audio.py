from __future__ import annotations
import pyxel


class AudioManager:
    _instance: "AudioManager | None" = None

    def __init__(self) -> None:
        self._initialized = False
        self._current_music: int | None = None

    @classmethod
    def get(cls) -> "AudioManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def init(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._define_sounds()
        self._define_music()

    @staticmethod
    def _s(idx: int, notes: str, tones: str, volumes: str, effects: str, speed: int) -> None:
        pyxel.sound(idx).set(notes, tones, volumes, effects, speed)

    def _define_sounds(self) -> None:
        # ── Opening BGM (snds 0-2): C major, bright adventure title ──
        # Melody: ascending C major arpeggio, descends gently
        self._s(0, "c3 e3 g3 e3 c4 b3 a3 g3 a3 g3 f3 e3 d3 c3 r r",
                "s", "7", "n", 8)
        # Harmony: thirds below melody
        self._s(1, "e2 g2 c3 g2 e3 d3 c3 b2 c3 b2 a2 g2 f2 e2 r r",
                "t", "5", "n", 8)
        # Bass: I-IV-V pattern with offbeat rhythm
        self._s(2, "c2 r r c2 r c2 f1 r r f1 r f1 g1 r r g1",
                "p", "6", "n", 8)

        # ── Stage 1 BGM (snds 4-6): C major, upbeat outdoor park ──
        # Melody: bouncy repeated motif, cheerful
        self._s(4, "g3 e3 c3 e3 g3 a3 g3 r g3 f3 e3 d3 c3 e3 g3 r",
                "s", "7", "n", 7)
        # Harmony: parallel thirds
        self._s(5, "e2 c2 g1 c2 e2 f2 e2 r e2 d2 c2 b1 g1 c2 e2 r",
                "t", "5", "n", 7)
        # Bass: steady I-IV-V stride
        self._s(6, "c2 r c2 r f1 r f1 r g1 r g1 r c2 r c2 r",
                "p", "6", "n", 7)

        # ── Stage 2 BGM (snds 8-10): A minor, dark castle dungeon ──
        # Melody: A minor scale with mysterious gaps (rests create tension)
        self._s(8, "a3 r g3 f3 e3 r d3 c3 b2 r c3 d3 e3 r f3 e3",
                "s", "7", "n", 10)
        # Harmony: sparse, low intervals
        self._s(9, "a2 r e2 d2 c2 r b1 a1 g1 r a1 b1 c2 r d2 c2",
                "t", "5", "n", 10)
        # Bass: i-VI-III-VII pedal pattern
        self._s(10, "a1 r r a1 r r f1 r r c1 r r e1 r r e1",
                "p", "6", "n", 10)

        # ── Stage 3 BGM (snds 12-14): E minor, intense rocky terrain ──
        # Melody: continuous sixteenth-note run, no rests — relentless pace
        self._s(12, "e3 d3 c3 b2 a2 b2 c3 d3 e3 f3 g3 f3 e3 d3 c3 b2",
                "s", "7", "n", 8)
        # Harmony: parallel motion half a step below
        self._s(13, "g2 f2 e2 d2 c2 d2 e2 f2 g2 a2 b2 a2 g2 f2 e2 d2",
                "t", "5", "n", 8)
        # Bass: driving i-v alternation
        self._s(14, "e1 r e1 r b1 r b1 r c1 r c1 r g1 r g1 r",
                "p", "6", "n", 8)

        # ── Stage 4 BGM (snds 16-18): D minor, epic space final boss ──
        # Melody: dramatic D minor with chromatic ascent
        self._s(16, "d3 r r d3 c3 b2 a2 r g2 a2 b2 c3 d3 e3 f3 e3",
                "s", "7", "n", 9)
        # Harmony: dark parallel motion
        self._s(17, "f2 r r f2 e2 d2 c2 r b1 c2 d2 e2 d2 r c2 d2",
                "t", "5", "n", 9)
        # Bass: deep i-v-VI-III progression
        self._s(18, "d1 r a1 r f1 r c1 r g1 r d1 r a1 r e1 r",
                "p", "6", "n", 9)

        # ── Game Over BGM (snds 20-22): C minor, sad descending ──
        # Melody: slow stepwise descent to silence
        self._s(20, "g3 f3 e3 d3 c3 b2 a2 g2 r r r r r r r r",
                "t", "7", "n", 12)
        # Harmony: third below, fading alongside melody
        self._s(21, "e2 d2 c2 b1 a1 g1 f1 e1 r r r r r r r r",
                "t", "5", "n", 12)
        # Bass: chromatic descent
        self._s(22, "c2 r b1 r a1 r g1 r f1 r e1 r c1 r r r",
                "p", "5", "n", 12)

        # ── Clear BGM (snds 24-26): C major, triumphant victory fanfare ──
        # Melody: soaring ascent to high C then triumphant descent
        self._s(24, "c3 e3 g3 c4 g3 e3 c3 r c4 b3 a3 g3 f3 e3 d3 c3",
                "s", "7", "n", 8)
        # Harmony: supporting thirds
        self._s(25, "e2 g2 c3 e3 c3 g2 e2 r e3 d3 c3 b2 a2 g2 f2 e2",
                "t", "5", "n", 8)
        # Bass: I-IV-V-I celebration
        self._s(26, "c2 r e1 r g1 r c2 r f1 r a1 r g1 r c2 r",
                "p", "6", "n", 8)

        # ── Sound Effects ──
        # 28: select — bright ascending chirp when starting
        self._s(28, "c3 e3 g3 c4", "ssss", "7654", "nnnn", 4)
        # 29: attack_dagger — fast high-pitched slash
        self._s(29, "b3 a3 g3 r", "ssss", "7430", "nssn", 3)
        # 30: attack_sword — heavier downward sweep
        self._s(30, "e3 f3 g3 a3 r r", "ssssss", "776500", "nnssnn", 4)
        # 31: attack_rod — magical sparkle with vibrato fade
        self._s(31, "c4 e4 g4 b4", "tttt", "7654", "nnvf", 3)
        # 32: bomb — noise burst explosion
        self._s(32, "a2 r r r", "nnnn", "7531", "nfff", 5)
        # 33: get — coin/key pickup ascending notes
        self._s(33, "c3 g3 c4 e4", "ssss", "7777", "nnnn", 4)
        # 34: castle — short victory fanfare when goal opens
        self._s(34, "c3 e3 g3 c4 e4 c4 r r", "ssssssss", "77777500", "nnnnnnnn", 5)
        # 35: transform — magic sweep with vibrato and fadeout
        self._s(35, "c3 d3 e3 f3 g3 a3 b3 c4", "tttttttt", "33445677", "nnnnvvvf", 4)
        # 36: thunder — noise double-strike lightning
        self._s(36, "c3 r r c3 r r r r", "nnnnnnnn", "74007400", "nnnnnnnn", 4)
        # 37: clash — metallic sword impact
        self._s(37, "f3 g3 f3 r", "ssss", "7650", "nssn", 4)

    def _define_music(self) -> None:
        # ch0=melody(sq), ch1=harmony(tri), ch2=bass(pulse), ch3=empty(reserved for SE)
        pyxel.music(0).set([0],  [1],  [2],  [])   # Opening
        pyxel.music(1).set([4],  [5],  [6],  [])   # Stage 1
        pyxel.music(2).set([8],  [9],  [10], [])   # Stage 2
        pyxel.music(3).set([12], [13], [14], [])   # Stage 3
        pyxel.music(4).set([16], [17], [18], [])   # Stage 4
        pyxel.music(5).set([20], [21], [22], [])   # Game Over
        pyxel.music(6).set([24], [25], [26], [])   # Clear

    _MUSIC_MAP: dict[str, int] = {
        "opening": 0,
        "stage1":  1,
        "stage2":  2,
        "stage3":  3,
        "stage4":  4,
        "gameover": 5,
        "clear":   6,
    }

    _SE_MAP: dict[str, int] = {
        "select":        28,
        "attack_dagger": 29,
        "attack_sword":  30,
        "attack_rod":    31,
        "bomb":          32,
        "get":           33,
        "castle":        34,
        "transform":     35,
        "thunder":       36,
        "clash":         37,
    }

    def play_bgm(self, key: str, loops: int = -1) -> None:
        mid = self._MUSIC_MAP.get(key)
        if mid is None:
            return
        self._current_music = mid
        pyxel.playm(mid, loop=True)

    def stop_bgm(self) -> None:
        if self._current_music is not None:
            pyxel.stop(0)
            pyxel.stop(1)
            pyxel.stop(2)
            self._current_music = None

    def play_se(self, key: str) -> None:
        snd = self._SE_MAP.get(key)
        if snd is not None:
            pyxel.play(3, snd)

    def bgm_key_for_stage(self, stage: int) -> str:
        return f"stage{stage}"
