# Labyrinth Tanks

A local two-player tank game built with Python and Pygame CE. Players race to
capture the flag in a randomly generated maze while firing at each other.

## Play from source

Python 3.10 or newer is required.

## Controls and rules

| Player | Movement | Fire |
| --- | --- | --- |
| Player 1 | W, A, S, D | Space |
| Player 2 | Arrow keys | Enter |

- Capture the flag three times to win.
- A hit sends the opposing tank back to its spawn.
- Press **R** to restart with a new random maze.
- Press **Esc** or close the window to quit.

## Build the Windows executable

The executable is a single windowed file, built for the current Windows
machine. Install the optional build dependency and run the build script:

The result is `Tanks.exe` in the project root, beside this README. It can be
copied and run on Windows systems without a separate Python installation.
Build it on Windows to produce a Windows executable.

## Project layout

```text
Tanks.exe             Standalone Windows game
README.md             Setup, controls, build, and test instructions
pyproject.toml        Package metadata and dependencies
tanks.py              Direct source-checkout launcher
src/tanksgame/
    __init__.py       Public package API
    __main__.py       Installed module/console entry point
    config.py         Display, arena, and color constants
    entities.py       Tank and bullet data models
    game.py           Match state, input, and simulation
    level.py          Maze generation and grid coordinates
    renderer.py       Pygame rendering and HUD
    theme.py          Random arena palettes and contrasting tank colors
tests/
    test_game.py      Match rules and restart behavior
    test_level.py     Random maze invariants
    test_theme.py     Map and tank color contrast
tools/
    build_exe.py      PyInstaller executable builder
```
