# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

There is no build system, package manager, or test suite. Open `hiyokoman_js/index.html` directly in a browser. Chrome is recommended; if sound errors occur, replace `hiyokoman_js/js/enchant.js` with the build from [enchant.js-builds](https://github.com/ghelia/enchant.js-builds).

## Architecture

This is a 2014 browser-based action game built on [enchant.js](https://github.com/wise9/enchant.js) (development stopped). All game classes are created with `enchant.Class.create` and extend enchant base classes (`enchant.Scene`, `enchant.Sprite`, `enchant.Map`).

**Script loading order matters.** `hiyokoman_js/index.html` loads `js/Main.js` first because it defines the global `game` object and all type constants referenced by every other file. The remaining scripts are loaded in dependency order.

### Global State (`hiyokoman_js/js/Main.js`)

All shared state lives on the `game` (`Core`) object:
- `game.stage` — current stage number (1–4)
- `game.score` — cumulative score
- `game.original` — boolean flag; when `true`, stage 1 spawns a monster using `original/character.png` and `original/sound3.wav` instead of the default slime

Type constants are plain globals: `YELLOW/RED/BLUE` (Hiyoko types), `DAGGER/SWORD/ROD` (weapons), `SLIME/BAT/WARM/ROCK/DRAGON/THUNDER/ORIGINAL` (monster types), `APPLE/BANANA/GRAPES` (drop items).

### Scene Flow

```
OpeningScene → BattleScene(1) → BattleScene(2) → BattleScene(3) → BattleScene(4)
                     ↓ (lose/time)                                        ↓ (win)
               GameOverScene                                         ClearScene
                     ↑ (item pickup triggers overlay then resumes)
               TransformScene
```

Scenes are managed with `game.pushScene` / `game.popScene`. `TransformScene` is pushed on top of `BattleScene` and popped immediately, acting as a brief animation overlay.

### BattleScene (`hiyokoman_js/js/BattleScene.js`)

The core game loop. All per-stage content (map tiles, monster nests, monster spawns, key positions, castle position, BGM) is selected via `switch(game.stage)` inside factory methods (`getNests`, `getMonsters`, `getKeys`, `getCastle`, `getBGM`, `getBackGround`). To add or modify stage content, edit these switch blocks.

Each frame, `BattleScene` runs collision detection between all active entity groups: Hiyoko↔Monster, Hiyoko↔Key, Hiyoko↔Castle, Hiyoko↔DropItem, Monster↔Weapon. Dead/inactive entities are removed by checking `visible == false`.

### Entities

| File | Class | Notes |
|------|-------|-------|
| `hiyokoman_js/js/Hiyoko.js` | `Hiyoko` | Player sprite; type determines image, weapon, and speed. Calls `new GameOverScene` on death. |
| `hiyokoman_js/js/Monster.js` | `Monster` | All monster types in one class, branched by `type`. WARM/DRAGON spawn projectile child monsters (ROCK/THUNDER) via `action()` return value, which `BattleScene` then adds to the scene. |
| `hiyokoman_js/js/Weapon.js` | `Weapon` | Projectile fired by Hiyoko; angle derived from current walking frame. |
| `hiyokoman_js/js/Nest.js` | `Nest` | Spawner that probabilistically creates new monsters each frame via `born()`. |
| `hiyokoman_js/js/Map.js` | `HiyokoMap` | Extends `enchant.Map`; tile data and `collisionData` hardcoded per stage. `isHit` wraps `hitTest` for wall collision; `isBroken` checks specific tile IDs for destructible tiles. |
| `hiyokoman_js/js/Key.js` | `Key` | Collectible; all keys must be collected before `Castle` becomes visible. |
| `hiyokoman_js/js/DropItem.js` | `DropItem` | Dropped by monsters on death; collecting APPLE/BANANA/GRAPES triggers `TransformScene` and changes Hiyoko type. |

### Sound Handling

enchant.js supports two audio backends. Both are handled wherever BGM is played:
- **WebAudioSound**: `game.assets[bgm].src` exists — play once and set `.src.loop = true`
- **DOMSound**: `game.assets[bgm].src` is falsy — call `.play()` every frame inside `ENTER_FRAME`

### Custom Character Mode

Set `game.original = true` in `hiyokoman_js/js/Main.js` to replace one stage-1 SLIME nest with an ORIGINAL-type monster that uses `hiyokoman_js/original/character.png` (32×32 sprite sheet) and `hiyokoman_js/original/sound3.wav`. The `hiyokoman_js/mapeditor/` directory contains standalone map data files not used by the main game.
