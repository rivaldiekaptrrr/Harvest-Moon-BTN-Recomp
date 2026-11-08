# Harvest Moon: Back to Nature — Native PC Port (Static Recompilation)

[![Platform](https://img.shields.io/badge/platform-Windows%20x64-blue.svg)](https://github.com)
[![Architecture](https://img.shields.io/badge/arch-MIPS%20to%20x86__64-orange.svg)](https://github.com)
[![Runtime](https://img.shields.io/badge/runtime-SDL3%20%7C%20OpenGL-brightgreen.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT%20(Code%20Only)-lightgrey.svg)](LICENSE)
[![Legal](https://img.shields.io/badge/release-Clean--Room%20Assetless-green.svg)](https://github.com)

A high-performance, native PC port of the beloved PlayStation 1 classic **Harvest Moon: Back to Nature (USA)**, built using ahead-of-time (AOT) static recompilation.

Unlike traditional emulation that interprets or JIT-compiles machine code at runtime, this project translates the original MIPS R3000A binary directly into optimized, native 64-bit C/C++ machine code. The result is zero emulation overhead, instant responsiveness, sub-millisecond input latency, and seamless support for modern displays and controllers.

---

## 🌟 Key Features

- **Native Execution**: Runs directly on your CPU and GPU as a standalone 64-bit Windows executable.
- **Indonesian Subtitle & Text Mode**: Built-in runtime translation system (`translations/harvest_moon_id.toml`) offering full Indonesian subtitles, menus, and item names without altering disc image data. Switchable on-the-fly via Launcher.
- **Modern Controller Support**: Automatic plug-and-play detection for Xbox Wireless Controllers, Bluetooth gamepads (X3, 8BitDo, iPega), DualShock 4, and DualSense controllers via SDL3.
- **DualShock & Digital Modes**: Full support for both D-Pad and Left Analog Stick movement.
- **Enhanced Video Engine**: Built on modern SDL3 and OpenGL, supporting custom internal resolutions and window modes.
- **Ultra-Lightweight**: Minimal CPU and RAM footprint compared to heavy emulators.
- **Clean-Room & Legal**: 100% assetless release bundled with the open-source **OpenBIOS** (MIT licensed). No copyrighted Sony or Natsume assets are distributed.

---

## 📋 System Requirements

| Component | Minimum | Recommended |
| :--- | :--- | :--- |
| **OS** | Windows 10 (64-bit) or Windows 11 | Windows 10/11 (64-bit) |
| **Processor** | Any x86_64 Dual-Core CPU (Intel/AMD) | Modern Quad-Core CPU |
| **Memory** | 512 MB RAM | 2 GB RAM |
| **Graphics** | OpenGL 3.3 compatible GPU | Modern Dedicated or Integrated GPU |
| **Storage** | ~250 MB free space (including disc image) | SSD storage |

---

## 🚀 Quick Start Guide

### Step 1: Download & Extract
Download the latest clean release archive (`HarvestMoonBTN_PC_Port_v1.0.0_CleanRelease.zip`) and extract it to your preferred directory.

### Step 2: Provide Your Game Disc Image
To comply with copyright laws, this release does not bundle the original game disc image. You must supply your own legal backup of **Harvest Moon: Back to Nature (USA)**:

1. Locate your game dump (`.cue` and `.bin`, or compressed `.chd`).
2. Copy them into the `game/` folder:
   ```text
   HarvestMoonBTN_PC_Release/
   ├── HarvestMoonBTN_Recompiled.exe
   ├── game.toml
   ├── input.ini
   ├── keybinds.ini
   ├── Play_Harvest_Moon_PC.bat
   └── game/
       ├── Harvest Moon - Back to Nature (USA).cue
       └── Harvest Moon - Back to Nature (USA).bin
   ```

> [!TIP]
> **Using Compressed CHD Format:**
> If you have a `.chd` disc image, place it in `game/` and update line 4 of `game.toml`:
> ```toml
> disc = "game/Harvest Moon - Back to Nature (USA).chd"
> ```

### Step 3: Launch & Configure
Double-click **`Play_Harvest_Moon_PC.bat`** (or run **`HarvestMoonBTN_Launcher.exe`**).

The graphical **Configuration Launcher** will appear, allowing you to configure:
- **Language / Subtitle**: Choose between `🇮🇩 Bahasa Indonesia (Subtitle & Menu)` and `🇺🇸 English (Original)`.
- **Display & Resolution**: Windowed, Borderless Fullscreen, Exclusive Fullscreen, Resolution presets (HD, Full HD, 2K, 4K), and Aspect Ratio (4:3 Classic, 16:9 Widescreen, 21:9 Ultrawide).
- **Graphics & FPS**: Target FPS (30, 60, 120, 144, 240 FPS), V-Sync (On/Off/Adaptive), PGXP 3D Geometry Precision, FXAA Anti-Aliasing, and Multi-threading.
- **Controls & Input**: Auto Xbox/Bluetooth Gamepad detection, Analog/Digital stick mode, and customizable analog deadzone.
- **Save Management**: Instant access to your memory card saves (`card1.mcd`).

Click **`▶ MAINKAN GAME`** to save your preferences and jump straight into Mineral Town!

---

## 🎮 Controls & Button Mapping

### Gamepad Controls (Xbox / Generic Layout)
Connected controllers are auto-detected on startup with zero configuration required:

| Xbox / Generic Input | PS1 Equivalent | In-Game Action |
| :--- | :--- | :--- |
| **D-Pad / Left Stick** | D-Pad / Analog Stick | Walk / Run / Menu Navigation |
| **Button A** | ✕ (Cross) | Confirm / Pick Up Item / Talk / Drop |
| **Button B** | ◯ (Circle) | Cancel / Hold to Run |
| **Button X** | ◻ (Square) | Use Equipped Tool (Hoe, Watering Can, Sickle) |
| **Button Y** | △ (Triangle) | Open Rucksack / Inventory |
| **LB (Left Bumper)** | L1 | Whistle to Call Dog |
| **RB (Right Bumper)** | R1 | Cycle / Switch Equipped Tool |
| **LT (Left Trigger)** | L2 | Whistle to Call Horse |
| **RT (Right Trigger)** | R2 | Quick Access Rucksack |
| **Start Button** | Start | Pause Game / View Farm Assets & Status |
| **Back Button** | Select | Open Town & Farm Map |

### Keyboard Controls (Fallback)

| Keyboard Key | In-Game Action |
| :--- | :--- |
| **Arrow Keys** | Movement (Up, Down, Left, Right) |
| **X** | Confirm / Pick Up [✕] |
| **S** | Cancel / Hold to Run [◯] |
| **Z** | Use Tool [◻] |
| **A** | Open Rucksack [△] |
| **Q / W** | L1 / R1 |
| **E / R** | L2 / R2 |
| **Enter (Return)** | Start Menu |
| **Right Shift** | Select (Map) |

> Custom button mappings can be adjusted at any time in [`input.ini`](input.ini) (for controllers) and [`keybinds.ini`](keybinds.ini) (for keyboard).

---

## ⚙️ Configuration (`game.toml`)

You can customize runtime and rendering behavior by editing `game.toml`:

```toml
[runtime]
window_title = "Harvest Moon: Back to Nature (PC Port)"
bios_hle = false
overlay_cache = true

[controller]
p1_device = "auto"     # Automatically connects first physical gamepad
p1_mode = "analog"     # "analog" (DualShock) or "digital" (Standard pad)
deadzone = 3277        # ~10% radial deadzone

[video]
renderer = "opengl"    # Graphics renderer: "opengl" or "vulkan"
```

---

## ⚖️ Legal Disclaimer

- This project is an independent clean-room static recompilation endeavor.
- **No copyrighted game assets, audio files, textures, or ROMs are included** in this release.
- **OpenBIOS** included in this distribution is licensed under the permissive **MIT License**.
- *Harvest Moon* and *Back to Nature* are registered trademarks of Marvelous Inc., Natsume Inc., and Sony Interactive Entertainment. All trademarks belong to their respective owners.
- Users must dump and provide their own legally acquired game disc image to play.

