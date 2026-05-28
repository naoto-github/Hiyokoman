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
        pyxel.sounds[idx].set(notes, tones, volumes, effects, speed)

    def _define_sounds(self) -> None:
        # ── Sound index layout ──────────────────────────────────────
        # Opening   ch0:0-1  ch1:2-3  ch2:4-5   (2 phrases, ~8.5s)
        # Stage 1   ch0:6-8  ch1:9-11 ch2:12-14 (3 phrases, ~11s)
        # Stage 2   ch0:15-17 ch1:18-20 ch2:21-23 (3 phrases, ~14s)
        # Stage 3   ch0:24-26 ch1:27-29 ch2:30-32 (3 phrases, ~10s)
        # Stage 4   ch0:33-35 ch1:36-38 ch2:39-41 (3 phrases, ~13s)
        # Game Over ch0:42  ch1:43  ch2:44   (1 phrase, ~7.5s, once)
        # Clear     ch0:45  ch1:46  ch2:47   (1 phrase, ~3.7s, once)
        # SE        48-57
        # ────────────────────────────────────────────────────────────

        # ── Opening BGM: C major, cheerful title screen ──────────────
        # speed 8 → 16 notes × 8/30 ≈ 4.3s per phrase  (2 phrases = ~8.5s loop)
        self._s( 0, "c3 e3 g3 c4 b3 g3 a3 c4 g3 e3 f3 a3 e3 c3 d3 r", "s", "7", "n", 8)
        self._s( 1, "f3 a3 c4 f4 e4 c4 a3 g3 e3 g3 b3 e4 d4 b3 c4 r", "s", "7", "n", 8)
        self._s( 2, "e2 g2 c3 e3 d3 b2 c3 e3 e2 c2 d2 f2 c2 a1 b1 r", "t", "5", "n", 8)
        self._s( 3, "d2 f2 a2 d3 c3 a2 f2 e2 g2 b2 d3 g3 f3 d3 e3 r", "t", "5", "n", 8)
        self._s( 4, "c1 r r c1 g1 r r g1 a1 r r a1 g1 r r r",          "p", "6", "n", 8)
        self._s( 5, "f1 r r f1 c1 r r c1 g1 r r g1 c1 r r r",          "p", "6", "n", 8)

        # ── Stage 1 BGM: C major, sunny meadow, upbeat ───────────────
        # speed 7 → 3 phrases = 48 notes × 7/30 ≈ 11.2s loop
        self._s( 6, "c3 e3 g3 c4 a3 g3 e3 g3 f3 a3 c4 f4 e4 c4 a3 r", "s", "7", "n", 7)
        self._s( 7, "g3 b3 d4 g4 f4 d4 b3 a3 g3 a3 b3 c4 d4 e4 f4 r", "s", "7", "n", 7)
        self._s( 8, "e3 f3 g3 a3 g3 f3 e3 d3 c3 e3 g3 c4 g3 e3 c3 r", "s", "7", "n", 7)
        self._s( 9, "e2 g2 c3 e3 f2 e2 c2 e2 d2 f2 a2 d3 c3 a2 f2 r", "t", "5", "n", 7)
        self._s(10, "e2 g2 b2 e3 d3 b2 g2 f2 e2 f2 g2 a2 b2 c3 d3 r", "t", "5", "n", 7)
        self._s(11, "c2 d2 e2 f2 e2 d2 c2 b1 a1 c2 e2 a2 e2 c2 a1 r", "t", "5", "n", 7)
        self._s(12, "c1 r c1 r f1 r f1 r g1 r g1 r c1 r r r",          "p", "6", "n", 7)
        self._s(13, "g1 r g1 r d1 r d1 r g1 r g1 r d1 r d1 r",         "p", "6", "n", 7)
        self._s(14, "a1 r a1 r g1 r g1 r c1 r c1 r c1 r r r",          "p", "6", "n", 7)

        # ── Stage 2 BGM: A minor, mysterious castle ──────────────────
        # speed 9 → 3 phrases = 48 notes × 9/30 ≈ 14.4s loop
        self._s(15, "a3 r c4 b3 a3 g3 f3 e3 d3 e3 f3 g3 a3 b3 c4 r",  "s", "7", "n", 9)
        self._s(16, "c4 b3 a3 g3 f3 e3 d3 c3 e3 a3 g3 f3 e3 d3 c3 r",  "s", "7", "n", 9)
        self._s(17, "e3 f3 g3 a3 b3 a3 g3 f3 e3 d3 c3 a2 c3 e3 a3 r",  "s", "7", "n", 9)
        self._s(18, "a2 r e3 d3 c3 b2 a2 g2 f2 g2 a2 b2 c3 d3 e3 r",   "t", "5", "n", 9)
        self._s(19, "e3 d3 c3 b2 a2 g2 f2 e2 c2 f2 e2 d2 c2 b1 a1 r",  "t", "5", "n", 9)
        self._s(20, "c2 d2 e2 f2 g2 f2 e2 d2 c2 b1 a1 f1 a1 c2 f2 r",  "t", "5", "n", 9)
        self._s(21, "a1 r r a1 e1 r r e1 d1 r r d1 e1 r r r",           "p", "6", "n", 9)
        self._s(22, "a1 r a1 r f1 r f1 r c1 r c1 r e1 r e1 r",          "p", "6", "n", 9)
        self._s(23, "e1 r e1 r d1 r d1 r c1 r c1 r a1 r r r",           "p", "6", "n", 9)

        # ── Stage 3 BGM: E minor, relentless rock drive ──────────────
        # speed 6 → 3 phrases = 48 notes × 6/30 ≈ 9.6s loop (fastest)
        self._s(24, "e3 f3 g3 a3 b3 a3 g3 f3 e3 d3 c3 d3 e3 f3 g3 e3", "s", "7", "n", 6)
        self._s(25, "b3 c4 d4 e4 d4 c4 b3 a3 g3 a3 b3 c4 b3 a3 g3 r",  "s", "7", "n", 6)
        self._s(26, "a3 g3 f3 e3 d3 e3 f3 g3 a3 b3 a3 g3 f3 e3 r r",   "s", "7", "n", 6)
        self._s(27, "b2 c3 d3 e3 f3 e3 d3 c3 b2 a2 g2 a2 b2 c3 d3 b2", "t", "5", "n", 6)
        self._s(28, "g3 a3 b3 c4 b3 a3 g3 f3 e3 f3 g3 a3 g3 f3 e3 r",  "t", "5", "n", 6)
        self._s(29, "f3 e3 d3 c3 b2 c3 d3 e3 f3 g3 f3 e3 d3 c3 r r",   "t", "5", "n", 6)
        self._s(30, "e1 r e1 r g1 r g1 r a1 r a1 r b1 r b1 r",          "p", "6", "n", 6)
        self._s(31, "e1 r b1 r d1 r a1 r g1 r e1 r b1 r r r",           "p", "6", "n", 6)
        self._s(32, "a1 r a1 r g1 r g1 r f1 r e1 r e1 r r r",           "p", "6", "n", 6)

        # ── Stage 4 BGM: D minor, epic space / final boss ────────────
        # speed 8 → 3 phrases = 48 notes × 8/30 ≈ 12.8s loop
        self._s(33, "d3 r d3 r f3 e3 d3 c3 b2 c3 d3 e3 f3 a3 g3 r",   "s", "7", "n", 8)
        self._s(34, "a3 b3 c4 d4 c4 b3 a3 g3 f3 g3 a3 b3 c4 d4 e4 r", "s", "7", "n", 8)
        self._s(35, "d4 c4 b3 a3 g3 f3 e3 d3 c3 d3 e3 f3 a3 f3 d3 r", "s", "7", "n", 8)
        self._s(36, "f2 r f2 r a2 g2 f2 e2 d2 e2 f2 g2 a2 c3 b2 r",   "t", "5", "n", 8)
        self._s(37, "f2 g2 a2 b2 a2 g2 f2 e2 d2 e2 f2 g2 a2 b2 c3 r", "t", "5", "n", 8)
        self._s(38, "b3 a3 g3 f3 e3 d3 c3 b2 a2 b2 c3 d3 f3 d3 b2 r", "t", "5", "n", 8)
        self._s(39, "d1 r r d1 a1 r r a1 f1 r r f1 c1 r r r",          "p", "6", "n", 8)
        self._s(40, "d1 r a1 r f1 r c1 r g1 r d1 r a1 r e1 r",         "p", "6", "n", 8)
        self._s(41, "d1 r d1 r c1 r c1 r f1 r f1 r d1 r r r",          "p", "6", "n", 8)

        # ── Game Over BGM: C minor, slow sad descent (plays once) ────
        # speed 14 → 16 notes × 14/30 ≈ 7.5s
        self._s(42, "g3 r f3 r e3 r d3 r c3 r b2 r a2 r g2 r", "t", "7", "n", 14)
        self._s(43, "e2 r d2 r c2 r b1 r a1 r g1 r f1 r e1 r", "t", "5", "n", 14)
        self._s(44, "c2 r r r a1 r r r f1 r r r c1 r r r",     "p", "5", "n", 14)

        # ── Clear BGM: C major, triumphant fanfare (plays once) ──────
        # speed 7 → 16 notes × 7/30 ≈ 3.7s
        self._s(45, "c3 e3 g3 c4 e4 g4 b4 r a4 g4 e4 c4 g3 e3 c3 r", "s", "7", "n", 7)
        self._s(46, "e2 g2 c3 e3 g3 c4 e4 r d4 b3 g3 e3 c3 g2 e2 r", "t", "5", "n", 7)
        self._s(47, "c1 r e1 r g1 r c1 r g1 r c1 r e1 r c1 r",        "p", "6", "n", 7)

        # ── Sound Effects (48-57) ─────────────────────────────────────
        self._s(48, "c3 e3 g3 c4",                   "ssss",     "7654",     "nnnn",     4)  # select
        self._s(49, "b3 a3 g3 r",                    "ssss",     "7430",     "nssn",     3)  # attack_dagger
        self._s(50, "e3 f3 g3 a3 r r",              "ssssss",   "776500",   "nnssnn",   4)  # attack_sword
        self._s(51, "c4 e4 g4 b4",                   "tttt",     "7654",     "nnvf",     3)  # attack_rod
        self._s(52, "a2 r r r",                      "nnnn",     "7531",     "nfff",     5)  # bomb
        self._s(53, "c3 g3 c4 e4",                   "ssss",     "7777",     "nnnn",     4)  # get
        self._s(54, "c3 e3 g3 c4 e4 c4 r r",        "ssssssss", "77777500", "nnnnnnnn", 5)  # castle
        self._s(55, "c3 d3 e3 f3 g3 a3 b3 c4",      "tttttttt", "33445677", "nnnnvvvf", 4)  # transform
        self._s(56, "c3 r r c3 r r r r",             "nnnnnnnn", "74007400", "nnnnnnnn", 4)  # thunder
        self._s(57, "f3 g3 f3 r",                    "ssss",     "7650",     "nssn",     4)  # clash

    def _define_music(self) -> None:
        pyxel.musics[0].set([0,  1   ], [2,  3   ], [4,  5   ], [])  # Opening
        pyxel.musics[1].set([6,  7,  8], [9,  10, 11], [12, 13, 14], [])  # Stage 1
        pyxel.musics[2].set([15, 16, 17], [18, 19, 20], [21, 22, 23], [])  # Stage 2
        pyxel.musics[3].set([24, 25, 26], [27, 28, 29], [30, 31, 32], [])  # Stage 3
        pyxel.musics[4].set([33, 34, 35], [36, 37, 38], [39, 40, 41], [])  # Stage 4
        pyxel.musics[5].set([42],         [43],         [44],         [])  # Game Over
        pyxel.musics[6].set([45],         [46],         [47],         [])  # Clear

    _MUSIC_MAP: dict[str, int] = {
        "opening":  0,
        "stage1":   1,
        "stage2":   2,
        "stage3":   3,
        "stage4":   4,
        "gameover": 5,
        "clear":    6,
    }

    _SE_MAP: dict[str, int] = {
        "select":        48,
        "attack_dagger": 49,
        "attack_sword":  50,
        "attack_rod":    51,
        "bomb":          52,
        "get":           53,
        "castle":        54,
        "transform":     55,
        "thunder":       56,
        "clash":         57,
    }

    def play_bgm(self, key: str, loops: int = -1) -> None:
        mid = self._MUSIC_MAP.get(key)
        if mid is None:
            return
        self._current_music = mid
        pyxel.playm(mid, loop=(loops != 0))

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
