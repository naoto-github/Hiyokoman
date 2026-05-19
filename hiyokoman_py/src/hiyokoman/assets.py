from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image

from .constants import ASSET_ROOT, TILE_SIZE
from .renderer import SpriteSheet, quantize


class Assets:
    _instance: "Assets | None" = None

    def __init__(self) -> None:
        # Hiyoko character sprite sheets [YELLOW, RED, BLUE]
        self.hiyoko: list[SpriteSheet] = []
        # Large opening-scene character images [YELLOW, RED, BLUE]
        self.hiyoko_big: list[tuple[np.ndarray, np.ndarray]] = []
        # Monster sprite sheets keyed by type constant
        self.monster: dict[int, SpriteSheet] = {}
        # Weapon sprite sheets keyed by type constant
        self.weapon: dict[int, SpriteSheet] = {}
        # Weapon icon sprite sheets [DAGGER, SWORD, ROD]
        self.weapon_icon: list[SpriteSheet] = []
        # Death / hit effect
        self.effect: SpriteSheet | None = None
        # Map tile sheets keyed by filename stem
        self.map_tiles: dict[str, SpriteSheet] = {}
        # Item / key icon sheet (icon0.png)
        self.icons: SpriteSheet | None = None
        # Precomputed map layers per stage {stage: (layer1, mask1, layer2, mask2)}
        self.map_layers: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}

    @classmethod
    def get(cls) -> "Assets":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self, map_data: "module") -> None:  # type: ignore[name-defined]
        """Load and quantize all game assets. map_data module provides stage arrays."""
        import pyxel
        from .constants import YELLOW, RED, BLUE, DAGGER, SWORD, ROD, PY_ASSET_ROOT
        root = ASSET_ROOT
        img = root / "images"

        # --- Opening background (image bank 0) ---
        bg_path = PY_ASSET_ROOT / "opening_bg.pyxres"
        if bg_path.exists():
            pyxel.load(
                str(bg_path),
                exclude_tilemaps=True,
                exclude_sounds=True,
                exclude_musics=True,
            )

        # --- Characters ---
        self.hiyoko = [
            SpriteSheet.load(str(img / "characters/hiyoco_normal_full.png"), 32, 32),
            SpriteSheet.load(str(img / "characters/hiyoco_lady_full.png"), 32, 32),
            SpriteSheet.load(str(img / "characters/hiyoco_waru_full.png"), 32, 32),
        ]

        for name in ["hiyoco_big.png", "hiyoco_big_lady.png", "hiyoco_big_waru.png"]:
            pil = Image.open(img / "characters" / name)
            # Scale to 128×128 for display
            pil = pil.resize((128, 128), Image.LANCZOS)
            self.hiyoko_big.append(quantize(pil))

        # --- Monsters ---
        from .constants import SLIME, BAT, WARM, DRAGON, ORIGINAL
        self.monster[SLIME]    = SpriteSheet.load(str(img / "monster/slime.gif"),  48, 48)
        self.monster[BAT]      = SpriteSheet.load(str(img / "monster/bat.gif"),    48, 48)
        self.monster[WARM]     = SpriteSheet.load(str(img / "monster/warm.gif"),   80, 80)
        self.monster[DRAGON]   = SpriteSheet.load(str(img / "monster/dragon.gif"), 80, 80)
        self.monster[ORIGINAL] = SpriteSheet.load(str(root / "original/character.png"), 32, 32)

        # ROCK uses map0 tile 27; THUNDER uses thunder.png (64×240 per frame)
        self.monster_map0_rock  = _tile_from_sheet(str(img / "map/map0.png"), 27, TILE_SIZE)
        self.monster_thunder    = SpriteSheet.load(str(img / "weapon/thunder.png"), 64, 240)

        # --- Weapons ---
        self.weapon[DAGGER] = SpriteSheet.load(str(img / "weapon/dagger.png"), 46, 46)
        self.weapon[SWORD]  = SpriteSheet.load(str(img / "weapon/cut.png"),    96, 96)
        self.weapon[ROD]    = SpriteSheet.load(str(img / "weapon/fire.png"),   96, 96)

        # Weapon icons (100×100 RGBA)
        for name in ["dagger_icon.png", "sword_icon.png", "rod_icon.png"]:
            pil = Image.open(img / "weapon" / name).resize((46, 46), Image.LANCZOS)
            px, mk = quantize(pil)
            self.weapon_icon.append(SpriteSheet(px, mk, 46, 46))

        # --- Effects ---
        self.effect = SpriteSheet.load(str(img / "monster/effect0.png"), 16, 16)

        # --- Map tiles ---
        for stem in ["map0", "map1"]:
            self.map_tiles[stem] = SpriteSheet.load(
                str(img / f"map/{stem}.png"), TILE_SIZE, TILE_SIZE
            )
        self.icons = SpriteSheet.load(str(img / "map/icon0.png"), TILE_SIZE, TILE_SIZE)

        # --- Precompute map layers for all stages ---
        for stage in range(1, 5):
            layer1_data = map_data.LAYER1[stage]
            layer2_data = map_data.LAYER2[stage]
            tile_sheet = self.map_tiles["map1"]
            l1, m1 = _build_map_layer(layer1_data, tile_sheet)
            l2, m2 = _build_map_layer(layer2_data, tile_sheet)
            self.map_layers[stage] = (l1, m1, l2, m2)


# --- Helpers ---

def _tile_from_sheet(
    path: str, tile_idx: int, tile_size: int
) -> tuple[np.ndarray, np.ndarray]:
    sheet = SpriteSheet.load(path, tile_size, tile_size)
    return sheet.frame(tile_idx)


def _build_map_layer(
    data: list[list[int]], sheet: SpriteSheet
) -> tuple[np.ndarray, np.ndarray]:
    rows, cols = len(data), len(data[0])
    H, W = rows * TILE_SIZE, cols * TILE_SIZE
    result   = np.zeros((H, W), dtype=np.uint8)
    result_m = np.zeros((H, W), dtype=bool)

    for r in range(rows):
        for c in range(cols):
            idx = data[r][c]
            if idx < 0:
                continue
            px, mk = sheet.frame(idx)
            dy, dx = r * TILE_SIZE, c * TILE_SIZE
            result_m[dy : dy + TILE_SIZE, dx : dx + TILE_SIZE] |= mk
            result[dy : dy + TILE_SIZE, dx : dx + TILE_SIZE][mk] = px[mk]

    return result, result_m
