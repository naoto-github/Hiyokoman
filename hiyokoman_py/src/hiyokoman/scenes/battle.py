from __future__ import annotations
import numpy as np
import pyxel

from .base import Scene
from ..constants import (
    YELLOW, RED, BLUE, DAGGER, SWORD, ROD,
    APPLE, BANANA, GRAPES,
    SLIME, BAT, WARM, DRAGON, ORIGINAL,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    STAGE_BG_COLOR,
)
from ..renderer import blit, fill, scaled_text
from ..assets import Assets
from ..audio import AudioManager
from ..game_state import GameState
from ..entities.hiyoko import Hiyoko
from ..entities.hiyoko_map import HiyokoMap
from ..entities.monster import Monster
from ..entities.weapon import Weapon
from ..entities.nest import Nest
from ..entities.key import Key
from ..entities.castle import Castle
from ..entities.drop_item import DropItem


class BattleScene(Scene):
    _TIME_LIMIT = 100  # seconds
    _TICKS_PER_SEC = 30

    def __init__(self, scenes: "SceneManager", stage: int) -> None:  # type: ignore[name-defined]
        super().__init__(scenes)
        state = GameState.get()
        state.stage = stage

        self._hmap = HiyokoMap(stage)
        self._hiyoko = Hiyoko(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, YELLOW, self._hmap)
        self._hiyoko.on_death(self._on_hiyoko_death)

        self._nests = self._make_nests(stage)
        self._castle = self._make_castle(stage)
        self._keys = self._make_keys(stage)
        self._monsters: list[Monster] = self._make_monsters(stage)
        self._weapons: list[Weapon] = []
        self._items: list[DropItem] = []

        self._ticks = 0
        self._time_left = self._TIME_LIMIT * self._TICKS_PER_SEC

        AudioManager.get().stop_bgm()
        AudioManager.get().play_bgm(f"stage{stage}")

    # ------------------------------------------------------------------ #
    #  Factory helpers                                                     #
    # ------------------------------------------------------------------ #

    def _make_nests(self, stage: int) -> list[Nest]:
        h, m = self._hiyoko, self._hmap
        state = GameState.get()
        cfg: dict[int, list[tuple]] = {
            1: [(60, 80, SLIME), (300, 160, SLIME),
                (80, 260, ORIGINAL if state.original else SLIME)],
            2: [(80, 110, BAT), (280, 60, SLIME), (70, 180, SLIME), (400, 30, BAT)],
            3: [(30, 50, BAT), (350, 270, SLIME), (250, 50, BAT)],
            4: [(110, 80, BAT), (270, 240, BAT)],
        }
        return [Nest(x, y, h, t, 0.01, m) for x, y, t in cfg.get(stage, [])]

    def _make_castle(self, stage: int) -> Castle:
        pos = {1: (350, 50), 2: (30, 280), 3: (280, 280), 4: (400, 280)}
        x, y = pos[stage]
        return Castle(x, y)

    def _make_keys(self, stage: int) -> list[Key]:
        cfg: dict[int, list[tuple]] = {
            1: [(20, 30), (400, 100), (300, 290)],
            2: [(125, 110), (172, 257), (250, 90)],
            3: [(60, 50), (120, 280), (440, 180)],
            4: [(20, 20), (440, 20), (20, 280)],
        }
        return [Key(x, y) for x, y in cfg.get(stage, [])]

    def _make_monsters(self, stage: int) -> list[Monster]:
        h, m = self._hiyoko, self._hmap
        if stage == 3:
            w1 = Monster(370, 20, h, WARM, m)
            w2 = Monster(40, 230, h, WARM, m)
            return [w1, w2]
        if stage == 4:
            w1 = Monster(330, 80, h, WARM, m)
            w2 = Monster(40, 250, h, WARM, m)
            d1 = Monster(20, 0, h, DRAGON, m)
            d2 = Monster(380, 0, h, DRAGON, m)
            return [w1, w2, d1, d2]
        return []

    # ------------------------------------------------------------------ #
    #  Update                                                              #
    # ------------------------------------------------------------------ #

    def update(self) -> None:
        self._ticks += 1
        self._time_left -= 1

        if self._time_left <= 0:
            self._trigger_gameover()
            return

        hiyoko = self._hiyoko
        hiyoko.update()

        # Attack
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z):
            self._fire_weapon()

        # Nest spawning
        for nest in self._nests:
            m = nest.born()
            if m:
                self._monsters.append(m)

        # Monster update — collect new projectiles
        new_proj: list[Monster] = []
        for m in self._monsters:
            proj = m.action()
            if proj:
                new_proj.append(proj)
        self._monsters.extend(new_proj)

        # Collisions
        self._check_hiyoko_monster()
        self._check_hiyoko_castle()
        self._check_hiyoko_keys()
        self._check_hiyoko_items()
        self._check_weapon_monster()

        # Update weapons
        for w in self._weapons:
            w.update()

        # Prune invisible entities
        self._monsters = [m for m in self._monsters if m.visible]
        self._weapons = [w for w in self._weapons if w.visible]
        self._items = [i for i in self._items if i.visible]

    def _fire_weapon(self) -> None:
        w = self._hiyoko.attack()
        self._weapons.append(w)
        se_map = {DAGGER: "attack_dagger", SWORD: "attack_sword", ROD: "attack_rod"}
        AudioManager.get().play_se(se_map[self._hiyoko.weapon_type])

    def _check_hiyoko_monster(self) -> None:
        h = self._hiyoko
        if not h.alive or GameState.get().invincible:
            return
        for m in self._monsters:
            if m.alive and m.is_hit(h):
                h.life -= m.attack_power
                AudioManager.get().play_se("bomb")

    def _check_hiyoko_castle(self) -> None:
        h = self._hiyoko
        c = self._castle
        if c.visible and h.within(c, c.radius):
            t = self._time_left // self._TICKS_PER_SEC
            from .clear import ClearScene
            AudioManager.get().stop_bgm()
            self._scenes.replace(ClearScene(self._scenes, h.htype, t))

    def _check_hiyoko_keys(self) -> None:
        h = self._hiyoko
        for key in self._keys:
            if key.active and h.within(key, key.radius):
                key.remove()
                h.key_count += 1
                if h.key_count >= len(self._keys):
                    self._castle.show()
                    AudioManager.get().play_se("castle")
                else:
                    AudioManager.get().play_se("get")

    def _check_hiyoko_items(self) -> None:
        h = self._hiyoko
        for item in self._items:
            if not item.active or not h.within(item, item.radius):
                continue
            item.remove()
            AudioManager.get().play_se("get")
            GameState.get().score += item.score

            if item.itype == APPLE and h.htype != RED:
                self._transform(h, RED)
            elif item.itype == BANANA and h.htype != YELLOW:
                self._transform(h, YELLOW)
            elif item.itype == GRAPES and h.htype != BLUE:
                self._transform(h, BLUE)

    def _transform(self, hiyoko: Hiyoko, new_type: int) -> None:
        from .transform import TransformScene
        self._scenes.push(TransformScene(self._scenes, hiyoko.htype, new_type))
        hiyoko.change(new_type)

    def _check_weapon_monster(self) -> None:
        for m in self._monsters:
            for w in self._weapons:
                if m.alive and w.active and m.within(w, w.radius):
                    w.attack(m)
                    AudioManager.get().play_se("bomb")
                    if not m.alive:
                        drop = m.drop()
                        if drop:
                            drop.show()
                            self._items.append(drop)

    def _on_hiyoko_death(self) -> None:
        from .gameover import GameOverScene
        AudioManager.get().stop_bgm()
        self._scenes.replace(GameOverScene(self._scenes, self._hiyoko.htype))

    def _trigger_gameover(self) -> None:
        from .gameover import GameOverScene
        AudioManager.get().stop_bgm()
        self._scenes.replace(GameOverScene(self._scenes, self._hiyoko.htype))

    # ------------------------------------------------------------------ #
    #  Draw                                                                #
    # ------------------------------------------------------------------ #

    def draw(self, screen: np.ndarray) -> None:
        state = GameState.get()
        assets = Assets.get()

        # Background fill
        bg = STAGE_BG_COLOR.get(state.stage, 0)
        fill(screen, bg)

        # Map layers
        if state.stage in assets.map_layers:
            l1, m1, l2, m2 = assets.map_layers[state.stage]
            blit(screen, l1, m1, 0, 0)
            blit(screen, l2, m2, 0, 0)

        # Nests
        for nest in self._nests:
            nest.draw(screen)

        # Castle
        self._castle.draw(screen)

        # Keys
        for key in self._keys:
            key.draw(screen)

        # Drop items
        for item in self._items:
            item.draw(screen)

        # Monsters
        for m in self._monsters:
            m.draw(screen)

        # Hiyoko
        self._hiyoko.draw(screen)

        # Weapons
        for w in self._weapons:
            w.draw(screen)

        # HUD
        self._draw_hud(screen)

    def _draw_hud(self, screen: np.ndarray) -> None:
        state = GameState.get()
        t_sec = max(0, self._time_left // self._TICKS_PER_SEC)
        scaled_text(screen, 2, 2, f"SCORE:{state.score}", 15)
        time_str = f"TIME:{t_sec:3d}"
        scaled_text(screen, SCREEN_WIDTH - 2 - len(time_str) * 8, 2, time_str, 15)

        wname = {DAGGER: "DAGGER", SWORD: "SWORD", ROD: "ROD"}
        wname_str = wname.get(self._hiyoko.weapon_type, "?")
        scaled_text(screen, SCREEN_WIDTH - 2 - len(wname_str) * 8, SCREEN_HEIGHT - 14, wname_str, 15)

        key_str = f"KEY:{self._hiyoko.key_count}/{len(self._keys)}"
        scaled_text(screen, 2, SCREEN_HEIGHT - 14, key_str, 15)
