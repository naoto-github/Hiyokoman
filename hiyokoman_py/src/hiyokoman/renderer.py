from __future__ import annotations
import numpy as np
from PIL import Image
import pyxel
from .constants import PALETTE, SCREEN_WIDTH, SCREEN_HEIGHT

# Pre-build palette RGB table for vectorized quantization
_PAL_RGB = np.array(
    [[(c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF] for c in PALETTE],
    dtype=np.float32,
)


def setup_palette() -> None:
    for i, color in enumerate(PALETTE):
        pyxel.colors[i] = color


def quantize(pil_image: Image.Image) -> tuple[np.ndarray, np.ndarray]:
    """Convert PIL image to (palette_indices H×W uint8, alpha_mask H×W bool)."""
    rgba = np.array(pil_image.convert("RGBA"), dtype=np.uint8)
    alpha_mask: np.ndarray = rgba[:, :, 3] > 0
    rgb = rgba[:, :, :3].astype(np.float32)

    # Vectorized nearest-palette-color via squared Euclidean distance
    diffs = rgb[:, :, None, :] - _PAL_RGB[None, None, :, :]  # H×W×16×3
    dists = np.sum(diffs**2, axis=3)                          # H×W×16
    indices = np.argmin(dists, axis=2).astype(np.uint8)       # H×W

    return indices, alpha_mask


def blit(
    dst: np.ndarray,
    sprite: np.ndarray,
    mask: np.ndarray,
    x: int,
    y: int,
) -> None:
    """Write sprite pixels (where mask is True) onto dst at (x, y)."""
    sh, sw = sprite.shape
    dh, dw = dst.shape

    dx0 = max(0, x);  dy0 = max(0, y)
    dx1 = min(dw, x + sw);  dy1 = min(dh, y + sh)
    if dx1 <= dx0 or dy1 <= dy0:
        return

    sx0, sy0 = dx0 - x, dy0 - y
    sx1, sy1 = sx0 + (dx1 - dx0), sy0 + (dy1 - dy0)

    m = mask[sy0:sy1, sx0:sx1]
    dst[dy0:dy1, dx0:dx1][m] = sprite[sy0:sy1, sx0:sx1][m]


def fill(dst: np.ndarray, color_idx: int) -> None:
    # Use numpy since pyxel.cls() was already called before the buffer was obtained
    dst[:, :] = color_idx


class SpriteSheet:
    """Precomputed quantized sprite sheet with frame extraction."""

    def __init__(
        self,
        pixels: np.ndarray,   # H×W uint8 palette indices
        mask: np.ndarray,     # H×W bool
        frame_w: int,
        frame_h: int,
    ) -> None:
        self.pixels = pixels
        self.mask = mask
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.cols = pixels.shape[1] // frame_w

    @classmethod
    def load(cls, path: str | None, frame_w: int, frame_h: int) -> "SpriteSheet":
        if path is None:
            blank = np.zeros((frame_h, frame_w), dtype=np.uint8)
            return cls(blank, np.zeros_like(blank, dtype=bool), frame_w, frame_h)
        img = Image.open(path)
        px, mk = quantize(img)
        return cls(px, mk, frame_w, frame_h)

    def frame(self, idx: int) -> tuple[np.ndarray, np.ndarray]:
        col = idx % self.cols
        row = idx // self.cols
        x, y = col * self.frame_w, row * self.frame_h
        return (
            self.pixels[y : y + self.frame_h, x : x + self.frame_w],
            self.mask[y : y + self.frame_h, x : x + self.frame_w],
        )

    def rotated_frame(self, idx: int, angle_deg: float) -> tuple[np.ndarray, np.ndarray]:
        px, mk = self.frame(idx)
        pil_px = Image.fromarray(px, mode="P")
        pil_mk = Image.fromarray(mk.astype(np.uint8) * 255)
        r_px = pil_px.rotate(angle_deg, expand=False)
        r_mk = pil_mk.rotate(angle_deg, expand=False)
        return np.array(r_px, dtype=np.uint8), np.array(r_mk) > 0
