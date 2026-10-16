# Tools

Everything used during the investigation, kept as it was used. The scripts
expect to be run **from this folder**, and they import each other by name.

```sh
./setup.sh /path/to/STONKERS.TAP     # venv + SkoolKit, patched tape, snapshots in ./work
./venv/bin/python vids2.py /tmp/crash.mp4               # the bridge crash (original game)
STONK=fixed ./venv/bin/python vids2.py /tmp/fixed.mp4   # same scene, patched game
```

Setting `STONK=fixed` makes every script run the patched game instead of the original.
You need `ffmpeg` on your PATH for videos and `magick` (ImageMagick) for some montages.

The game itself isn't included. The tape tested was the common TAP image with MD5
`f0c54d9f56300e177f47c62618493c2d`.

## The emulator harness

| File | What it is |
|---|---|
| `harness.py` | A scriptable 48K Spectrum built on SkoolKit's C Z80 simulator: keyboard matrix, frame stepping, snapshots, screenshots, optional video |
| `recorder.py` | Renders screen RAM straight to RGB and pipes it to ffmpeg (MP4) |
| `ui.py` | Plays the game like a person: puts the X cursor on a unit, presses fire, steers |
| `exp.py`, `exp3.py`, `exp7.py`, `fuzz2.py` | Helpers: inject routes, aim/zoom the view, place units after the game has started |
| `monitor.py` | Flags any execution inside data areas (unit tables, screen, ROM `RST $38`) |

## Reproducing the bug

| File | What it does |
|---|---|
| `demo.py`, `vids2.py` | The staged bridge scene: a low-supply armoured division ordered across the bridge |
| `fuzz4.py` | Statistics: moving units running out of supplies near the bridge (crash / survived / not triggered) |
| `fuzz5.py` | The same, sampled over the whole map |
| `battle.py`, `play.py` | Automated full battles: the whole army marches across the bridge to the enemy HQ and port |
| `battle2.py`, `rep2.py`, `replay.py`, `step.py`, `junk.py` | Re-run a crashing battle with an action log and checkpoints, then single-step into the crash |
| `endings.py`, `endings2.py` | Force each of the four end-of-battle conditions and check the next battle starts |
| `vid1.py`, `vidbattle.py` | The gameplay video and the full-battle video |

## The exploration, roughly in order

`tapls.py`, `extract.py`, `basic.py` (taking the tape apart) · `t1.py`–`t6.py` (driving
the menus) · `dumpattr.py`, `findbytes.py`, `hexd.py`, `terr.py`, `terrstat.py` (memory
spelunking: terrain map, tile banks, thresholds) · `exp2.py`–`exp12.py` (bridge-crossing
experiments) · `fuzz.py`, `fuzz3.py` (fuzzers) · `repro.py`, `repro2.py`, `trace1.py`–`trace4.py`
(how `fuzz.py`'s edits to the start-position table exposed the latent `$DE0D` bug) ·
`fuzz6.py` (a steering-pattern comparison that never got run; the decisive clue arrived first).

Some of the exploratory scripts read files that earlier ones produce: `t6.py` writes
`work/ingame.z80` and `work/map2.txt`, and the disassembly lives in `work/g.skool`. They
are kept as a record of the hunt rather than as polished tools.
