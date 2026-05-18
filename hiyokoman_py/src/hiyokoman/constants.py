from pathlib import Path

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FPS = 30
DISPLAY_SCALE = 2
TILE_SIZE = 16

# Hiyoko types
YELLOW = 0
RED = 1
BLUE = 2

# Weapon types
DAGGER = 0
SWORD = 1
ROD = 2

# Monster types
SLIME = 0
BAT = 1
WARM = 2
ROCK = 3
DRAGON = 4
THUNDER = 5
ORIGINAL = 6

# Drop item types
APPLE = 0
BANANA = 1
GRAPES = 2

# Custom 16-color palette (0xRRGGBB) covering game sprites
PALETTE: list[int] = [
    0x000000,  # 0: black (outlines)
    0x1a0c04,  # 1: very dark brown (bat outline)
    0x4434a7,  # 2: dark purple (slime body)
    0x8996ff,  # 3: light purple (slime highlight)
    0x60c249,  # 4: bright green (map grass)
    0x3f9fff,  # 5: blue (map water)
    0x685342,  # 6: dark brown (bat/terrain)
    0x9f9f9f,  # 7: gray (stone/bat wing)
    0xae561e,  # 8: dark orange-brown (hiyoko outline)
    0xf5a65a,  # 9: orange (hiyoko body)
    0xf9d27d,  # 10: light orange (hiyoko shading)
    0xffffb4,  # 11: very light yellow (hiyoko highlight)
    0xc95047,  # 12: red (dragon/effects)
    0xffa300,  # 13: bright orange (fire/items)
    0xffffa3,  # 14: yellow (effects/items)
    0xffffff,  # 15: white (highlights/text)
]

# Background fill color index per stage
STAGE_BG_COLOR: dict[int, int] = {
    1: 4,   # green (park)
    2: 6,   # dark brown (castle)
    3: 7,   # gray (rock)
    4: 0,   # black (space)
}

# Asset root: hiyokoman_js/ directory at the repo root
ASSET_ROOT = Path(__file__).parents[3] / "hiyokoman_js"
