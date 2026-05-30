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
    def _m(idx: int, mml: str) -> None:
        pyxel.sounds[idx].mml(mml)

    # ─────────────────────────────────────────────────────────────────
    # Sound layout
    #   Opening  : snd  0- 5  (A+B × 3ch)  T125  7.68s × 2 = 15.36s loop
    #   Stage 1  : snd  6-11  (A+B × 3ch)  T145  6.62s × 2 = 13.24s loop
    #   Stage 2  : snd 12-17  (A+B × 3ch)  T100  9.60s × 2 = 19.20s loop
    #   Stage 3  : snd 18-23  (A+B × 3ch)  T155  6.19s × 2 = 12.38s loop
    #   Stage 4  : snd 24-29  (A+B × 3ch)  T110  8.73s × 2 = 17.45s loop
    #   Gameover : snd 30-32  (1ph × 3ch)  T80   12.00s  (plays once)
    #   Clear    : snd 33-35  (1ph × 3ch)  T145   6.62s  (plays once)
    #   SE       : snd 36-45
    #
    # Each phrase:  melody = 32 × L8,  harmony = 16 × L4,  bass = 8 × L2
    # All three channels share the same BPM → identical total_sec.
    # ch3 is left empty in every music so SE can play uninterrupted there.
    # ─────────────────────────────────────────────────────────────────
    def _define_sounds(self) -> None:

        # ── Opening BGM: C major, T125, welcoming adventure ──────────
        # A phrase: I – IV – V – I  (bars 1-4)
        self._m(0,  # melody A  (32 L8, square)
            "T125 @1 V110 L8"
            " O3 C E G > C E D C < B"
            " O3 F A > C F < A F D B"
            " O3 G B > D G < B G E D"
            " O3 C E G > C < A G E C")
        self._m(1,  # melody B  (32 L8) — vi-ii-V-I
            "T125 @1 V110 L8"
            " O3 A > C E A < G E C A"
            " O3 D F A > D < F D B G"
            " O3 G B > D G F E D < B"
            " O3 C E G > C < G E C G")
        self._m(2,  # harmony A  (16 L4, triangle)
            "T125 @0 V70 L4"
            " O3 E G C E"
            " O3 A C F A"
            " O3 B G D B"
            " O3 C G E C")
        self._m(3,  # harmony B
            "T125 @0 V70 L4"
            " O3 A E C A"
            " O3 D F A D"
            " O3 B D G B"
            " O3 G E C G")
        self._m(4,  # bass A  (8 L2, pulse)
            "T125 @2 V90 L2 O2 C G F C G D C G")
        self._m(5,  # bass B
            "T125 @2 V90 L2 O2 A E D A G D C G")

        # ── Stage 1 BGM: C major, T145, sunny upbeat park ────────────
        # A phrase: C – Am – G – C
        self._m(6,  # melody A
            "T145 @1 V110 L8"
            " O3 C E G > C E D C < B"
            " O3 A > C E A G E D C"
            " O3 G B > D G F E D < B"
            " O3 C E G > C < A G E C")
        self._m(7,  # melody B — scalar runs
            "T145 @1 V110 L8"
            " O4 C D E F G A G F"
            " O4 E D C < B O3 A G F E"
            " O3 F G A > C D < B A G"
            " O3 E G > C E < A G E C")
        self._m(8,  # harmony A
            "T145 @0 V70 L4"
            " O3 G E C G"
            " O3 E C A E"
            " O3 B G D B"
            " O3 G E C G")
        self._m(9,  # harmony B
            "T145 @0 V70 L4"
            " O4 E D C O3 B"
            " O3 A G F E"
            " O3 B D G B"
            " O3 G E C G")
        self._m(10, # bass A
            "T145 @2 V90 L2 O2 C G A E G D C G")
        self._m(11, # bass B
            "T145 @2 V90 L2 O2 C G F C G D C G")

        # ── Stage 2 BGM: A minor, T100, mysterious dark castle ────────
        # A phrase: Am – G – F – Em
        self._m(12, # melody A
            "T100 @1 V110 L8"
            " O3 A B > C D E D C < B"
            " O3 G A B > C D C < B A"
            " O3 F G A B > C < B A G"
            " O3 E F G A B A G F")
        self._m(13, # melody B — descend then climb
            "T100 @1 V110 L8"
            " O4 E D C < B O3 A G F E"
            " O3 D E F G A B > C D"
            " O3 C < B A G F E D E"
            " O3 A B > C E D C < B A")
        self._m(14, # harmony A
            "T100 @0 V65 L4"
            " O3 A E C A"
            " O3 G D B G"
            " O3 F C A F"
            " O3 E G B E")
        self._m(15, # harmony B
            "T100 @0 V65 L4"
            " O3 C A E C"
            " O3 D F A D"
            " O3 B E G B"
            " O3 A E C A")
        self._m(16, # bass A
            "T100 @2 V90 L2 O2 A E G D F C E A")
        self._m(17, # bass B
            "T100 @2 V90 L2 O2 E C D A G E A E")

        # ── Stage 3 BGM: E minor, T155, relentless rocky terrain ──────
        # A phrase: no rests — continuous motion
        self._m(18, # melody A
            "T155 @1 V110 L8"
            " O3 E F# G A B A G F#"
            " O3 G B > D E < B G E D"
            " O3 A B > C D E < B A G"
            " O3 G A B > E D < B G E")
        self._m(19, # melody B
            "T155 @1 V110 L8"
            " O4 E D C < B O3 A G F# E"
            " O3 G A B > C D E F# G"
            " O3 A G F# E D E F# G"
            " O3 B > E D < B A G E F#")
        self._m(20, # harmony A
            "T155 @0 V65 L4"
            " O3 E G B E"
            " O3 B G E G"
            " O3 A E C A"
            " O3 G B E G")
        self._m(21, # harmony B
            "T155 @0 V65 L4"
            " O3 B G E B"
            " O3 G D B G"
            " O3 E C A E"
            " O3 G E B G")
        self._m(22, # bass A
            "T155 @2 V90 L2 O2 E B B F# A E G B")
        self._m(23, # bass B
            "T155 @2 V90 L2 O2 E B G D A E E B")

        # ── Stage 4 BGM: D minor, T110, epic space / final boss ───────
        # A phrase: Dm – Gm – Am – Dm  (dramatic and heavy)
        self._m(24, # melody A
            "T110 @1 V110 L8"
            " O3 D F A > D C < A F D"
            " O3 G B > D G F D < B G"
            " O3 A > C E A G E C < A"
            " O3 D F A > D F D < A F")
        self._m(25, # melody B — chromatic ascent
            "T110 @1 V110 L8"
            " O4 D C < A F D F A > D"
            " O3 A B > C D E F G A"
            " O3 B > C D E F G A > C"
            " O3 D F A > D F A D R")
        self._m(26, # harmony A
            "T110 @0 V65 L4"
            " O3 D A F D"
            " O3 G D B G"
            " O3 A E C A"
            " O3 F A D F")
        self._m(27, # harmony B
            "T110 @0 V65 L4"
            " O3 F D A F"
            " O3 A E C A"
            " O3 G D B G"
            " O3 D F A D")
        self._m(28, # bass A
            "T110 @2 V90 L2 O2 D A G D A E F A")
        self._m(29, # bass B
            "T110 @2 V90 L2 O2 F D A E G D D A")

        # ── Game Over BGM: C minor, T80, slow sad descent ─────────────
        # Single 4-bar phrase, plays once
        # 16 beats × (60/80) = 12.0s — all three channels must match.
        self._m(30, # melody  (T80, 16 beats using L4/L2/dot)
            "T80 @0 V100"
            " O3 G2. R4 F4 E4 D4 C4"
            " O2 A2. R4 G2 R2")
        self._m(31, # harmony  (T80, 4 whole notes = 4×3s = 12s)
            "T80 @0 V65 O2 C1 G1 F1 C1")
        self._m(32, # bass  (T80, 4 whole notes)
            "T80 @2 V90 O1 C1 G1 F1 C1")

        # ── Clear BGM: C major, T145, triumphant fanfare ──────────────
        # Single 4-bar phrase, plays once
        # 16 beats × (60/145) = 6.62s — all channels match.
        self._m(33, # melody  (T145, 16 L4 beats)
            "T145 @1 V110 O4 L4"
            " C E G > C"
            " < G E C E"
            " G A F A"
            " G2 C2")
        self._m(34, # harmony  (16 L4)
            "T145 @0 V70 O3 L4"
            " E G C E"
            " G E C G"
            " F A F A"
            " G E C G")
        self._m(35, # bass  (8 L2)
            "T145 @2 V90 L2 O2 C G C G F C G C")

        # ── Sound Effects (snd 36-45) ─────────────────────────────────

        # 36: select — bright ascending chirp
        self._m(36, "T200 @1 V110 O4 L16 C E G > C")

        # 37: attack_dagger — fast high slash, quick gate
        self._m(37, "T200 @1 Q50 V110 O4 L16 B A G R")

        # 38: attack_sword — heavier sweep
        self._m(38, "T160 @1 Q65 V100 O4 L16 E F G A R R")

        # 39: attack_rod — triangle magic sparkle with vibrato
        self._m(39, "T200 @0 @VIB1{0,14,60} V100 O4 L16 C E G > C")

        # 40: bomb — noise burst explosion with envelope decay
        self._m(40, "T120 @3 @ENV1{110,8,70,16,0} O2 L4 A R")

        # 41: get — coin/key pickup jingle
        self._m(41, "T200 @1 V110 O4 L16 C G > C E")

        # 42: castle — short triumphant fanfare
        self._m(42, "T160 @1 V110 O4 L8 C E G > C E C")

        # 43: transform — magic sweep ascending with vibrato
        self._m(43, "T180 @0 @VIB1{12,20,100} V100 O3 L16 C D E F G A B > C")

        # 44: thunder — noise double strike
        self._m(44, "T120 @3 V110 O3 L16 A R A R R R R R")

        # 45: clash — metallic impact
        self._m(45, "T200 @1 Q60 V100 O4 L16 F G F R")

    def _define_music(self) -> None:
        # ch0=melody(sq), ch1=harmony(tri), ch2=bass(pulse), ch3=empty for SE
        pyxel.musics[0].set([0,  1 ], [2,  3 ], [4,  5 ], [])   # Opening
        pyxel.musics[1].set([6,  7 ], [8,  9 ], [10, 11], [])   # Stage 1
        pyxel.musics[2].set([12, 13], [14, 15], [16, 17], [])   # Stage 2
        pyxel.musics[3].set([18, 19], [20, 21], [22, 23], [])   # Stage 3
        pyxel.musics[4].set([24, 25], [26, 27], [28, 29], [])   # Stage 4
        pyxel.musics[5].set([30],     [31],     [32],     [])   # Game Over
        pyxel.musics[6].set([33],     [34],     [35],     [])   # Clear

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
        "select":        36,
        "attack_dagger": 37,
        "attack_sword":  38,
        "attack_rod":    39,
        "bomb":          40,
        "get":           41,
        "castle":        42,
        "transform":     43,
        "thunder":       44,
        "clash":         45,
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
