# 🕹️ Silent Hill 5: Homecoming — Camera Fix

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Documentação-Português%20(PT--BR)-009c3b?style=for-the-badge&logo=readme&logoColor=white" alt="Versão em Português"></a>
  <a href="README-EN.md"><img src="https://img.shields.io/badge/Documentation-English-0052cc?style=for-the-badge&logo=readme&logoColor=white" alt="English Version"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Status-100%25%20Functional-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Platform-PC%20Windows-0078D6?style=for-the-badge&logo=windows" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="License">
</p>

Definitive camera fix mod for the controller (gamepad) right stick, smart character-following camera, and independent vertical and aiming sensitivity for **Silent Hill 5: Homecoming (PC)**, developed, calibrated, and tested by **Emerson Teles**.

---

## 📋 Table of Contents

1. [Overview & Compatibility](#-overview--compatibility)
2. [Download Version 1.0.0](#-download-version-100)
3. [Files & Package Structure](#-files--package-structure)
4. [Step-by-Step Installation](#-step-by-step-installation)
5. [INI Configuration (Sensitivities)](#-ini-configuration-sensitivities)
6. [Supported Values, Decimals & Scaling](#-supported-values-decimals--scaling)
7. [Normal Camera Calculation & Vertical Calibration](#-normal-camera-calculation--vertical-calibration)
8. [Aiming & Character Following](#-aiming--character-following)
9. [Memory Protection Fix (Pre-Menu Crash)](#-memory-protection-fix-pre-menu-crash)
10. [Original Backup & Restoration](#-original-backup--restoration)
11. [Source Code & Build](#-source-code--build)
12. [Credits & Authorship](#-credits--authorship)
13. [About the Author & Official Links](#-about-the-author--official-links)

---

## 🌟 Overview & Compatibility

**Version 1.0.0 • Mod by Emerson Teles — EMERSON TELES**.

On the PC release of *Silent Hill: Homecoming*, gamepad camera controls suffer from severe native issues: sluggish right-stick responsiveness, an unpleasant quadratic vertical acceleration curve, desynchronization between camera turning and Alex Shepherd's character body, and locked aiming sensitivity (*Precision* camera).

This mod completely resolves these shortcomings:
- **Responsive & Natural Horizontal Turning:** The character's body and camera rotate in unison through the native engine routine, calculating camera angle directly from actual character direction.
- **Linear & Calibrated Vertical Response:** Eliminates the squared controller input curve, providing smooth, linear vertical aiming and viewing. Default vertical sensitivity (1.0) is calibrated to match the natural feel of horizontal rotation.
- **Independent Aiming Sensitivity:** Enables separate customization of horizontal and vertical sensitivity while aiming weapons (*Precision* camera), without altering standard exploration camera speeds.
- **Simple INI Configuration:** Customize speeds with ease via `camera_axis_fix.ini`.
- **Compatibility:** Developed and verified on the **Unknown Project 3.20** installation of *Silent Hill: Homecoming*.

---

## 📥 Download Version 1.0.0

### [⬇️ Download Silent Hill 5 Camera Fix v1.0.0 (ZIP)](https://github.com/Emertels/Silent-Hill-5-Camera-Fix/releases/download/v1.0.0/Silent-Hill-5-Camera-Fix-v1.0.0.zip)

> [!IMPORTANT]
> The release ZIP package contains **only the functional game files** required for installation (`Files/Bin`) and the original backup folder (`Files/_Backup Original`). All documentation and manuals are maintained here on the official GitHub repository page.

---

## 📂 Files & Package Structure

The functional mod package is structured as follows:

```text
Files/
├── Bin/
│   ├── g_SilentHill.sgl          # The only modified game binary with turning, aiming, and vertical hooks
│   ├── xinput1_3.dll             # Native wrapper reading INI and applying memory constants
│   ├── camera_input_base.dll     # Native input DLL for XInput forwarding
│   └── camera_axis_fix.ini       # Sensitivity configuration file
└── _Backup Original/
    └── Bin/
        └── g_SilentHill.sgl      # Preserved original file for safe restoration/uninstallation
```

> [!NOTE]
> The main executable (`SilentHill.exe`), `shv.dll`, `.PAK` archives, community translations, and save files remain completely untouched.

---

## 🛠️ Step-by-Step Installation

### Step 1: Preventive Backup
Close the game. Optionally back up your game's `Bin` directory and the configuration files `Engine/binds_pc_mjs.cfg` and `Engine/bindcfgs_pc.cfg`.

### Step 2: Copy Package Files
Copy all files from `Files/Bin` into your game installation's `Bin` folder, overwriting `g_SilentHill.sgl` when prompted.

### Step 3: Configure Right Stick Bindings
Open both `Engine/binds_pc_mjs.cfg` and `Engine/bindcfgs_pc.cfg` in a text editor (such as Notepad or VS Code). Locate the bindings below and ensure they are configured exactly as follows:

```text
setbind 1 COMMAND_CAMERA_X CONTROLLER 0 AXIS_RX -1.0 1.0 1.0
setbind 1 COMMAND_CAMERA_Y CONTROLLER 0 AXIS_RY -1.0 1.0 1.0
setbind 1 COMMAND_TURNLEFT DEVICE_INVALID 0 0
setbind 1 COMMAND_TURNRIGHT DEVICE_INVALID 0 0
```

> [!TIP]
> **Why disable stick TURNLEFT and TURNRIGHT?**
> Because the mod coordinates character turning seamlessly with camera rotation, leaving `COMMAND_TURNLEFT` and `COMMAND_TURNRIGHT` mapped to the right stick would stack two simultaneous turning commands. Setting them to `DEVICE_INVALID` ensures smooth and uniform rotation. Preserve all keyboard `addbind` entries and other commands.

### Step 4: Play and Enjoy
Launch the game and enjoy smooth, responsive controls!

---

## ⚙️ INI Configuration (Sensitivities)

With the game closed, edit `Bin/camera_axis_fix.ini`. The default configuration is:

```ini
; Patch Fix Camera 1.0 - By Emerson Teles
; Silent Hill: Homecoming - Unknown Project 3.20
[Camera]

; Normal horizontal camera and character turning (1.0 = 1.5 rad/s reference)
HorizontalCameraSpeed=1.0

; Normal vertical camera (1.0 calibrated to match horizontal feel)
VerticalCameraSpeed=1.0

; Aiming (Precision camera) - horizontal sensitivity
AimHorizontalSpeed=1.0

; Aiming (Precision camera) - vertical sensitivity
AimVerticalSpeed=1.0

; Legacy options (keep 1.0 for neutral response)
RightStickXExponent=1.0
RightStickYExponent=1.0
RightStickXGain=1.0
RightStickYGain=1.0
```

- `HorizontalCameraSpeed`: Speed of horizontal normal camera and character turning. Does not alter walking or running speeds.
- `VerticalCameraSpeed`: Speed of vertical normal camera. Default 1.0 already includes the doubled calibration factor ($2.864789$) to match horizontal feel.
- `AimHorizontalSpeed`: Horizontal multiplier applied exclusively while aiming firearms (Precision camera).
- `AimVerticalSpeed`: Vertical multiplier applied exclusively while aiming firearms (Precision camera).

---

## 📊 Supported Values, Decimals & Scaling

The main options accept decimal values from **0.25 to 3.0** with a dot (`.`):

| Value | Change vs. Default | Description |
| :---: | :---: | :--- |
| `0.25` | −75% | Extremely slow camera |
| `0.50` | −50% | Half the default speed |
| `0.75` | −25% | Moderate / smooth response |
| `1.00` | **Default** | **Calibrated and approved default sensitivity** |
| `1.20` | +20% | Slightly faster |
| `1.50` | +50% | Nimble and agile response |
| `2.00` | +100% | Double default speed |
| `2.50` | +150% | Very fast response |
| `3.00` | +200% | Maximum recommended speed |

> [!NOTE]
> Save the file and restart the game after modifying the INI to apply your changes.

---

## 📐 Normal Camera Calculation & Vertical Calibration

- **Horizontal:** Requests `1.5 × HorizontalCameraSpeed × input × dt` radians per frame. At 1.0 and maximum stick deflection, the reference speed is ~85.94 degrees per second.
- **Vertical:** The vanilla game squared controller input ($0.5^2 = 0.25$), causing a heavy feel near center and runaway acceleration at full deflection. The mod takes the absolute magnitude (`ANDPD`), making response linear while preserving deadzones, directions, and frame timing.
- **Calibration:** Native SGL constants are 60 deg/s at `VA 0x10F91290` and radian conversion `0.01745329` at `VA 0x10F93F48`, with a base gain of $1.432394$. To align vertical feel with horizontal 1.0, the mod applies an empirical calibration factor approved by Emerson Teles, yielding an effective gain of $2.864789 \times \text{VerticalCameraSpeed}$.

---

## 🎯 Aiming & Character Following

- Aiming applies `setting / 3.0` scaling immediately after the native curve output, triggering **strictly when Precision camera mode is active**.
- This eliminates the erratic overshooting of earlier prototypes and provides predictable, gradual aiming control.
- When the right stick is neutral, native smooth following behind the character remains fully preserved.

---

## 🛡️ Memory Protection Fix (Pre-Menu Crash)

During development, memory crash dumps (`SilentHill.exe.20612.dmp`) revealed a critical `0xC0000005` (Access Violation) exception when instruction VA `0x10386303` attempted to write to `0x103863F8`. That address resided inside `g_SilentHill.sgl`'s write-protected executable section.

The implemented solution:
1. Moved the `PrecisionMode` state flag into writable memory inside the proxy DLL (`xinput1_3.dll`).
2. Added null pointer checks inside the detour assembly hooks.
3. Ensured memory pages are restored to strict execute-only protection (`PAGE_EXECUTE_READ`) after applying hooks.
4. Verified via x86 native regression tests and page protection unit tests.

---

## 💾 Original Backup & Restoration

The repository preserves the original game file prior to any modifications:

- **File:** `Files/_Backup Original/Bin/g_SilentHill.sgl`
- **SHA256 Hash:** `2A7C30031A3146036115292EED7D6022C603470C257A5659BED8D4423F2DFD61`

> [!NOTE]
> This binary was compared against two identical older copies from the Unknown Project 3.20 installation and validated by Emerson Teles. Since only `g_SilentHill.sgl` was modified, reverting is immediate.

### How to Uninstall or Restore the Original Game:
1. **Close the game** completely.
2. Copy `Files/_Backup Original/Bin/g_SilentHill.sgl` to your game's `Bin` directory, overwriting the modded file.
3. Delete the mod's auxiliary files from the game's `Bin` directory:
   - `camera_axis_fix.ini`
   - `camera_input_base.dll`
   - `xinput1_3.dll`
4. Your original bindings and default game behavior will be 100% restored.

---

## 💻 Source Code & Build

The [`Source/`](Source/) directory contains full C/C++ proxy source code and tooling:

- `src/camera_xinput_proxy.cpp`: Interception wrapper and runtime injector.
- `src/camera_input_base.c`: Native input translation layer.
- `build_test/`: Automated signature verification and page-protection regression tests.
- `work/`: Python mathematical emulation, offset reconstruction, and validation scripts.

---

## ✍️ Credits & Authorship

- **Creation, Calibration, In-Game Testing & Organization:** **Emerson Teles (EMERSON TELES)**
- **Technical Implementation & Verification:** Emerson Teles with assistance from Codex
- **Version:** 1.0.0
- **License:** [MIT](LICENSE)

*Silent Hill: Homecoming* and *Unknown Project* are intellectual properties of their respective copyright holders. This is a non-profit, independent fan-made mod.

---

## 👨‍💻 About the Author & Official Links

Developed and maintained by **Emerson Teles** (known in the community as **Emertels**).

Tech enthusiast, system maintenance specialist, gamer, and technical software localizer into Brazilian Portuguese (PT-BR). Developer focused on practical utilities, productivity tools, PowerShell automation, and technical PC gaming mods.

### 🌐 Connect with Me & Official Communities

<div align="left">

[![GitHub](https://img.shields.io/badge/GitHub-Emertels-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/emertels)
[![Website](https://img.shields.io/badge/Website-Emerson_Teles-0070F3?style=for-the-badge&logo=googlechrome&logoColor=white)](https://emertels.github.io)
[![Discord](https://img.shields.io/badge/Discord-Emertels%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://emertels.github.io/discord)
[![X / Twitter](https://img.shields.io/badge/X_Twitter-@emertels-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/emertels)
[![YouTube](https://img.shields.io/badge/YouTube-Emerson_Teles-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@emersonteles2379)
[![Telegram](https://img.shields.io/badge/Telegram-Aplicativos%20Mods-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/apksmodsandroid)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Apoiar%20Projeto-FF5E5B?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/emertels)

</div>
