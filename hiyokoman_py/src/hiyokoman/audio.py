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
        # ── Pyxel octave note: c1=C3(130Hz) c2=C4(261Hz) c3=C5(523Hz) ──
        # Melody  range: c2-c3  (standard C4-C5, 261-523 Hz)
        # Harmony range: c1-c2  (standard C3-C4, 130-261 Hz)
        # Bass    range: c0-b0  (standard C2-B2,  65-123 Hz)
        #
        # Slot layout:
        #   Opening  0-5   (3ch × 2 phrases, ~8.5s)
        #   Stage 1  6-14  (3ch × 3 phrases, ~11s)
        #   Stage 2  15-23 (3ch × 3 phrases, ~14s)
        #   Stage 3  24-32 (3ch × 3 phrases, ~10s)
        #   Stage 4  33-41 (3ch × 3 phrases, ~13s)
        #   Gameover 42-44 (1 phrase, ~7.5s, plays once)
        #   Clear    45-47 (1 phrase, ~3.7s, plays once)
        #   SE       48-57

        # ── Opening BGM: C major, welcoming ──────────────────────────
        self._s( 0, "c2 e2 g2 e2 c3 b2 a2 g2 f2 a2 c3 b2 a2 g2 f2 r", "s", "7", "n", 8)
        self._s( 1, "g2 b2 d3 g3 f3 d3 b2 g2 a2 c3 e3 c3 a2 g2 e2 r", "s", "7", "n", 8)
        self._s( 2, "e1 g1 c2 g1 a1 d2 f2 e2 d2 f2 a2 g2 f2 e2 d2 r", "t", "5", "n", 8)
        self._s( 3, "b1 d2 g2 b2 a2 g2 d2 b1 c2 e2 g2 e2 d2 c2 b1 r", "t", "5", "n", 8)
        self._s( 4, "c0 r r c0 f0 r r f0 g0 r r g0 c0 r r r",          "p", "6", "n", 8)
        self._s( 5, "g0 r r g0 d0 r r d0 a0 r r a0 c0 r r r",          "p", "6", "n", 8)

        # ── Stage 1 BGM: C major, sunny and upbeat ───────────────────
        self._s( 6, "c2 e2 g2 c3 a2 g2 e2 c2 f2 a2 c3 a2 g2 e2 c2 r", "s", "7", "n", 7)
        self._s( 7, "g2 b2 d3 g3 f3 d3 b2 g2 a2 c3 b2 a2 g2 f2 e2 r", "s", "7", "n", 7)
        self._s( 8, "e2 g2 b2 e3 d3 b2 g2 e2 f2 a2 c3 a2 g2 e2 c2 r", "s", "7", "n", 7)
        self._s( 9, "e1 g1 c2 e2 f1 c2 a1 e1 d1 f1 a1 f2 e2 c2 a1 r", "t", "5", "n", 7)
        self._s(10, "b1 d2 g2 b2 a2 g2 d2 b1 c2 e2 g2 e2 c2 b1 g1 r", "t", "5", "n", 7)
        self._s(11, "c2 e2 g2 c3 b2 g2 e2 c2 d2 f2 a2 f2 e2 c2 a1 r", "t", "5", "n", 7)
        self._s(12, "c0 r c0 r f0 r f0 r g0 r g0 r c0 r r r",          "p", "6", "n", 7)
        self._s(13, "g0 r g0 r d0 r d0 r a0 r a0 r e0 r e0 r",         "p", "6", "n", 7)
        self._s(14, "a0 r a0 r g0 r g0 r c0 r c0 r c0 r r r",          "p", "6", "n", 7)

        # ── Stage 2 BGM: A minor, mysterious castle ──────────────────
        self._s(15, "a2 r c3 b2 a2 g2 f2 e2 d2 e2 f2 g2 a2 b2 c3 r",  "s", "7", "n", 9)
        self._s(16, "c3 b2 a2 g2 f2 e2 d2 c2 e2 a2 g2 f2 e2 d2 c2 r",  "s", "7", "n", 9)
        self._s(17, "e2 f2 g2 a2 b2 a2 g2 f2 e2 d2 c2 a1 c2 e2 a2 r",  "s", "7", "n", 9)
        self._s(18, "a1 r e2 d2 c2 b1 a1 g1 f1 g1 a1 b1 c2 d2 e2 r",   "t", "5", "n", 9)
        self._s(19, "e2 d2 c2 b1 a1 g1 f1 e1 c1 f1 e1 d1 c1 b0 a0 r",  "t", "5", "n", 9)
        self._s(20, "c1 d1 e1 f1 g1 f1 e1 d1 c1 b0 a0 f0 a0 c1 f1 r",  "t", "5", "n", 9)
        self._s(21, "a0 r r a0 e0 r r e0 d0 r r d0 e0 r r r",           "p", "6", "n", 9)
        self._s(22, "a0 r a0 r f0 r f0 r c0 r c0 r e0 r e0 r",          "p", "6", "n", 9)
        self._s(23, "e0 r e0 r d0 r d0 r c0 r c0 r a0 r r r",           "p", "6", "n", 9)

        # ── Stage 3 BGM: E minor, relentless drive ───────────────────
        self._s(24, "e2 f2 g2 a2 b2 a2 g2 f2 e2 d2 c2 d2 e2 f2 g2 e2", "s", "7", "n", 6)
        self._s(25, "b2 c3 d3 e3 d3 c3 b2 a2 g2 a2 b2 c3 b2 a2 g2 r",  "s", "7", "n", 6)
        self._s(26, "a2 g2 f2 e2 d2 e2 f2 g2 a2 b2 a2 g2 f2 e2 r r",   "s", "7", "n", 6)
        self._s(27, "b1 c2 d2 e2 f2 e2 d2 c2 b1 a1 g1 a1 b1 c2 d2 b1", "t", "5", "n", 6)
        self._s(28, "g2 a2 b2 c3 b2 a2 g2 f2 e2 f2 g2 a2 g2 f2 e2 r",  "t", "5", "n", 6)
        self._s(29, "f2 e2 d2 c2 b1 c2 d2 e2 f2 g2 f2 e2 d2 c2 r r",   "t", "5", "n", 6)
        self._s(30, "e0 r e0 r g0 r g0 r a0 r a0 r b0 r b0 r",          "p", "6", "n", 6)
        self._s(31, "e0 r b0 r d0 r a0 r g0 r e0 r b0 r r r",           "p", "6", "n", 6)
        self._s(32, "a0 r a0 r g0 r g0 r f0 r e0 r e0 r r r",           "p", "6", "n", 6)

        # ── Stage 4 BGM: D minor, epic space / final boss ────────────
        self._s(33, "d2 r d2 r f2 e2 d2 c2 b1 c2 d2 e2 f2 a2 g2 r",   "s", "7", "n", 8)
        self._s(34, "a2 b2 c3 d3 c3 b2 a2 g2 f2 g2 a2 b2 c3 d3 e3 r", "s", "7", "n", 8)
        self._s(35, "d3 c3 b2 a2 g2 f2 e2 d2 c2 d2 e2 f2 a2 f2 d2 r", "s", "7", "n", 8)
        self._s(36, "f1 r f1 r a1 g1 f1 e1 d1 e1 f1 g1 a1 c2 b1 r",   "t", "5", "n", 8)
        self._s(37, "f1 g1 a1 b1 a1 g1 f1 e1 d1 e1 f1 g1 a1 b1 c2 r", "t", "5", "n", 8)
        self._s(38, "b2 a2 g2 f2 e2 d2 c2 b1 a1 b1 c2 d2 f2 d2 b1 r", "t", "5", "n", 8)
        self._s(39, "d0 r r d0 a0 r r a0 f0 r r f0 c0 r r r",          "p", "6", "n", 8)
        self._s(40, "d0 r a0 r f0 r c0 r g0 r d0 r a0 r e0 r",         "p", "6", "n", 8)
        self._s(41, "d0 r d0 r c0 r c0 r f0 r f0 r d0 r r r",          "p", "6", "n", 8)

        # ── Game Over BGM: C minor, slow descent (plays once) ────────
        self._s(42, "g2 r f2 r e2 r d2 r c2 r b1 r a1 r g1 r", "t", "7", "n", 14)
        self._s(43, "e1 r d1 r c1 r b0 r a0 r g0 r f0 r e0 r", "t", "5", "n", 14)
        self._s(44, "c1 r r r a0 r r r f0 r r r c0 r r r",     "p", "5", "n", 14)

        # ── Clear BGM: C major, triumphant fanfare (plays once) ──────
        self._s(45, "c2 e2 g2 c3 e3 g3 b3 r a3 g3 e3 c3 g2 e2 c2 r", "s", "7", "n", 7)
        self._s(46, "e1 g1 c2 e2 g2 c3 d3 r e3 d3 c3 a2 e2 c2 a1 r", "t", "5", "n", 7)
        self._s(47, "c0 r e0 r g0 r c1 r g0 r c1 r g0 r c0 r",        "p", "6", "n", 7)

        # ── Sound Effects (48-57) ─────────────────────────────────────
        self._s(48, "c2 e2 g2 c3",                   "ssss",     "7654",     "nnnn",     4)  # select
        self._s(49, "b2 a2 g2 r",                    "ssss",     "7430",     "nssn",     3)  # attack_dagger
        self._s(50, "e2 f2 g2 a2 r r",              "ssssss",   "776500",   "nnssnn",   4)  # attack_sword
        self._s(51, "c3 e3 g3 b3",                   "tttt",     "7654",     "nnvf",     3)  # attack_rod
        self._s(52, "a1 r r r",                      "nnnn",     "7531",     "nfff",     5)  # bomb
        self._s(53, "c2 g2 c3 e3",                   "ssss",     "7777",     "nnnn",     4)  # get
        self._s(54, "c2 e2 g2 c3 e3 c3 r r",        "ssssssss", "77777500", "nnnnnnnn", 5)  # castle
        self._s(55, "c2 d2 e2 f2 g2 a2 b2 c3",      "tttttttt", "33445677", "nnnnvvvf", 4)  # transform
        self._s(56, "c2 r r c2 r r r r",             "nnnnnnnn", "74007400", "nnnnnnnn", 4)  # thunder
        self._s(57, "f2 g2 f2 r",                    "ssss",     "7650",     "nssn",     4)  # clash

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
