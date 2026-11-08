# HarvestMoonBTN

Generated locally by PSXRecomp from your own disc and BIOS.

## Build

Install CMake, Ninja, and a C/C++ compiler. SDL3 is fetched automatically.
Then run `.\build.ps1` in PowerShell.

This project must keep the generated `psxrecomp/` framework folder beside
`CMakeLists.txt`.

SDL3 is the default. To use SDL2 explicitly, configure once with
`cmake -S . -B build -DPSX_SDL_BACKEND=SDL2`; later build-script runs
preserve that cached selection.

The executable is written under `build/`. Keep your original disc image
at the path stored in `game.toml`, or update that path before running.

