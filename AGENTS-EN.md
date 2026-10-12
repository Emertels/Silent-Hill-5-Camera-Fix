# Patch Fix Camera 1.0 - By Emerson Teles — AGENTS

## Maintenance rules

Preserve public version 1.0, EMERSON TELES credits and user-selected filenames. Back up before changes; preserve personal INI values. Do not recalibrate approved horizontal motion, aiming or following without evidence. Distinguish formulas, simulated tests and user validation. Do not promise physical parity or compatibility with untested binaries. Do not publish automatically to GitHub.

Current state uses vertical calibration 2; earlier descriptions of equal X/Y angular requests refer to the previous base, not the current default. Approved gameplay after the crash fix does not establish visual comparison of the latest vertical normalization.

## Turning and vertical hooks

`work/build_navigation_response.py` composes the existing alignment. Main yaw VA `0x108DB3D6`, cave `0x10386000` and helper `0x10386100` preserve approved alignment. Turning uses native routine `0x10145F50`; yaw derives from effective direction through `_CIatan2`, with normalization and the original convention. `FXSAVE/FXRSTOR` preserves FPU/SSE. Do not redesign this path to adjust aiming.

Controller pitch at `0x10386200`: `CVTSS2SD XMM1,[EBX+24]`, `ANDPD` with absolute mask at `0x103862D0`, `MULSD` by native constant 60 and double gain at `0x103862F0`, return `0x108DB003`. EBX is the controller frame and XMM0 contains dt. Squaring was removed in this path; native decisions and the alternative path are preserved. The reference header contains base gain 1.4323944989229112 and calibration 2, whose effective product is 2.8647889978458223.

## Aiming hooks and writable state

Input hook `0x103851E0`, cave `0x10386300`: fixes reference 2 in fields `+AE8/AEC` only for the Precision camera. `0x103863F8` contains a pointer to `precision_mode` in writable DLL data. Each pass checks for a non-null pointer, clears state and sets it to 1 for Precision. Reference constant 2 is at `0x103863FC`.

The wrapper writes setting/3 at `0x103863F0/F4`. X: site `0x10711F24`, cave `0x10386400`, scales local `[ESP+20]` and replays `MOVSS XMM0,[0x10F8A2E4]`. Y: site `0x1071EA28`, cave `0x10386480`, scales XMM0 and replays store `[ESP+1C]`. `PUSHFD/POPFD` preserves flags from the previous CMP; registers and stack must remain correct. Never write mutable state into the executable page. Preserve null-pointer checks and protection restoration.

## Signatures, tests and evidence

The wrapper verifies hooks, main/helper, pitch, mask, aiming input, fixed reference and outputs before configuring gains. Do not relax verification to accept another SGL without analysis.

Test sources: `build_test/navigation_speed_smoke.c`, `build_test/camera_protection_smoke.c`, `work/smoke_camera_response.py` and `work/smoke_navigation_aligned.py`. The real protection regression executes x86 READ/EXECUTE code with writable state; emulation uses internal-routine stubs. After code changes, run relevant checks and test gameplay. Do not repeat tests without a change or concrete risk.

Failure evidence: `work/menu_crash_dump_report.json`, dump `SilentHill.exe.20612.dmp`, write `0x10386303 → 0x103863F8`, C0000005. The failed build was separated before the fix. Do not run `install_camera_v1_public.py` or other historical installers assuming they represent current state.

## Overview and compatibility

**Version 1.0 • Updated October 12, 2026 • Mod by Emerson Teles — EMERSON TELES**.

Controller fix for the normal camera, character following and independent aiming sensitivity. Developed and tested with this **Unknown Project 3.20** installation of Silent Hill: Homecoming. Other versions and the game without the mod have not been validated.

Emerson approved horizontal turning and following behind the character at 1.0 and 2.0. After the pre-menu crash was fixed, he also approved aiming at 1.0 and 2.0 and the overall response at 2.0. The latest vertical normalization still needs an in-game comparison: new vertical 1.0 matches the gain of previous vertical 2.0. This is the mod's calibrated default, not certification of exact equivalence to the original game.

## Files and scope

The installation package contains four files in `Files/Bin`:

1. `g_SilentHill.sgl`: the only existing game binary modified; contains the corrected turning, following, vertical and aiming paths.
2. `xinput1_3.dll`: the mod wrapper; reads the INI, verifies signatures, configures constants in memory and forwards XInput functions.
3. `camera_input_base.dll`: the native input DLL, required for forwarding and optional stick input adjustments.
4. `camera_axis_fix.ini`: configuration for the four sensitivities, with English comments and mod credits.

Both CFG files in `Engine` also require the bindings described below. They were adjusted in earlier revisions. During the latest vertical calibration, only the main DLL changed behavior; the INI received organization and comments. The SGL and CFGs remain unchanged; the base DLL provides native input. The executable, shv.dll, PAK, translation and saves are outside this update.

## Installation in three steps

1. Close the game. Back up the `Bin` files and `Engine/binds_pc_mjs.cfg` and `Engine/bindcfgs_pc.cfg`. Preserve any existing personal DLLs and INI files with the same names.
2. Copy all four files from `Files/Bin` into the compatible game's `Bin`. In both CFG files, find commands by name and keep the following right-stick bindings:

```text
setbind 1 COMMAND_CAMERA_X CONTROLLER 0 AXIS_RX -1.0 1.0 1.0
setbind 1 COMMAND_CAMERA_Y CONTROLLER 0 AXIS_RY -1.0 1.0 1.0
setbind 1 COMMAND_TURNLEFT DEVICE_INVALID 0 0
setbind 1 COMMAND_TURNRIGHT DEVICE_INVALID 0 0
```

Preserve keyboard `addbind` entries and other commands. The mod turns the body with the camera; the stick's TURNLEFT/TURNRIGHT bindings must be disabled to avoid adding another turn. Which CFG is loaded for every Unknown Project option has not been established; keep both consistent.

3. Start the game and test continuous turning in both directions, standing and walking, vertical motion and aiming. Start at 1.0, change one option at a time and restart after editing.

## Every INI option

Edit `Bin/camera_axis_fix.ini` with the game closed. The four package defaults are:

```ini
[Camera]
HorizontalCameraSpeed=1.0
VerticalCameraSpeed=1.0
AimHorizontalSpeed=1.0
AimVerticalSpeed=1.0
```

- `HorizontalCameraSpeed`: Normal horizontal camera and character turning; 1.5 rad/s reference at 1.0. Does not change walking or running speed.
- `VerticalCameraSpeed`: Normal vertical camera; new 1.0 equals previous 2.0. Effective gain 2.864788997846 × setting.
- `AimHorizontalSpeed`: Independent horizontal Precision camera sensitivity; multiplier applied after the native curve.
- `AimVerticalSpeed`: Independent vertical Precision camera sensitivity; multiplier applied after the native curve.
- `RightStickXExponent`: Legacy horizontal input curve; keep 1.0 for a neutral response.
- `RightStickYExponent`: Legacy vertical input curve; keep 1.0 for a neutral response.
- `RightStickXGain`: Legacy raw horizontal input gain; keep 1.0 to avoid stacking gains.
- `RightStickYGain`: Legacy raw vertical input gain; keep 1.0 to avoid stacking gains.

Keep CFG X/Y multipliers at 1.0 and adjust sensitivity through the INI. Changing both stacks gains. Legacy fields exist for compatibility with the earlier DLL; they do not replace the four main settings.

## Values, percentages and parsing

The four main options accept decimals from **0.25 to 3.0**, including 1.1, 1.15, 1.2, 1.5, 2.0 and 2.5. Use a decimal point; commas, negative signs and exponents are not accepted. Missing values or invalid text use 1.0. Ordinary out-of-range values are clamped; integers exceeding 100 during parsing may fall back to 1.0. Zero does not disable the mod. The main options' range does not apply to legacy fields.

Relative to 1.0: 0.25 = −75%; 0.5 = −50%; 0.75 = −25%; 1.1 = +10%; 1.2 = +20%; 1.5 = +50%; 2.0 = +100%; 2.5 = +150%; 3.0 = +200%. Formula: `(value - 1) × 100%`. Between settings: `(new / previous - 1) × 100%`; 1.1 to 1.2 is approximately +9.09%, and 2.0 to 2.5 is +25%.

These percentages describe gain, not guaranteed final visible speed. The log rounds values to two decimal places, but this does not limit parsed precision. Options are loaded at initialization: save and close/restart the game. See [MANUAL.md](MANUAL.md) for further examples and tips in Portuguese.

## Normal camera calculation and vertical calibration

Horizontal motion requests `1.5 × HorizontalCameraSpeed × input × dt` radians per frame. At 1.0 and full deflection, the reference is approximately 85.94 degrees/s. The native routine can limit actual turning; the camera follows the character's effective direction.

Original vertical input was squared: 0.5 became 0.25. The mod uses absolute input in the controller path for a linear response while preserving native direction handling, deadzone, frame time and limits.

References extracted from the SGL: 60 degrees/s at VA `0x10F91290` and radians conversion `0.01745329238474369` at VA `0x10F93F48`. Base gain is `1.5 / (60 × 0.01745329238474369) = 1.4323944989229112`.

Emerson selected previous vertical 2.0 as the baseline closest in feel to horizontal 1.0. Current calibration applies a factor of 2: effective gain `2.8647889978458223 × VerticalCameraSpeed`. Before limits, Y requests a maximum `3 × setting` rad/s; X requests `1.5 × setting`. These are therefore not equal physical rates. The adjustment is empirical, based on the user's test.

New Y1.0 = previous Y2.0; new Y1.5 = previous Y3.0. New Y2.0 and Y3.0 mathematically match previous Y4.0 and Y6.0 gains, which were not accepted by the previous INI. The current range remains 0.25–3.0. Test new 1.0 before increasing. Framing, collision, limits and actual turning can change perception.

## Aiming and character following

Aiming uses `setting / 3` after the identified native curve paths, only when the active camera is `Precision`: 1.0 = one third of the earlier fast reference; 2.0 = two thirds; 3.0 = the earlier fast reference, equivalent to previous 1.0 in these paths.

Earlier attempts increased input before the quadratic curve, making 2.0 excessively fast. Post-curve application provides proportional progression at the modified point. Engine acceleration, limits and other states can still affect motion; global final aiming degrees/s have not been measured. Other camera names do not receive these gains.

Changing only the horizontal CFG did not solve sluggishness; other attempts accelerated the weapon or turned the camera without the body. The approved solution turns the character through the native routine and calculates camera angle from the actual direction, using the original angular convention. At neutral input it retains original following. The latest vertical normalization preserved approved horizontal and aiming behavior.

## Pre-menu crash and verification

The `SilentHill.exe.20612.dmp` dump identified the original `0xC0000005` exception: a write by instruction VA `0x10386303` to address `0x103863F8`. The Precision flag was inside the SGL's protected executable section. The final `0xC0000409` exception in KERNELBASE was the subsequent termination.

The flag now resides in writable DLL data. The SGL contains a pointer configured by the wrapper; hooks check for a null pointer. After constants and the pointer are applied, pages return to their original protection. The DLL does not rewrite the SGL on disk.

The x86 build, native signature/value/forwarding test and real-detour test using `PAGE_EXECUTE_READ` passed, covering a null world, Precision, Navigation and an unconfigured pointer. Recorded emulation checks covered 255 curve/scale cases and 10,800 alignment frames. Simulated internals do not certify every game state. Emerson confirmed startup and good gameplay after the fix; the latest vertical normalization still awaits a visual comparison.

The `Bin/camera_axis_fix.log` log records signature application or rejection and aiming `post-curve scale=value/3`.

## Backup and restoration

`Files/_Backup Original/Bin/g_SilentHill.sgl` is the oldest pre-existing backup of this installation, SHA256 `2A7C30031A3146036115292EED7D6022C603470C257A5659BED8D4423F2DFD61`. It is not a certified vanilla file.

Close the game and restore the appropriate SGL and previous CFGs/auxiliary files. Remove the mod's two DLLs and INI only if they did not previously exist; personal files must be restored from personal backups.

Local record: pre-normalization backup at `C:/Projetos/SilentHill5-CameraFix/_backup/antes_normalizar_vertical_v1_20261012_125613`; pre-crash-fix backup at `_backup/antes_correcao_fechamento_v1_20261012_012327`; failed build archived at `_backup/falha_menu_v1_20261012`. These local records are not necessarily included in the public package.

## Sources and documentation

`Source` contains mod sources, headers, historical patch generators and tests; it does not contain the game's source code. The wrapper was rebuilt from the package and both native tests passed. See [Source/README.md](Source/README.md) and [Source/README.en.md](Source/README.en.md).

Historical generators still depend on compatible paths and backup/intermediate images. They are not a portable one-click generator. Do not blindly execute historical installers: they can install obsolete or failed versions. Do not publish backups or original binaries as source code. Public version remains 1.0; official GitHub repository: https://github.com/Emertels/Silent-Hill-5-Camera-Fix.

Paired documents: [README-PT-BR.md](README-PT-BR.md), [AGENTS.PT-BR.md](AGENTS.PT-BR.md) and [AGENTS-EN.md](AGENTS-EN.md). [MANUAL.md](MANUAL.md) details options and tests in Portuguese; [CHANGELOG.md](CHANGELOG.md) records changes; `SHA256.json` identifies files.

## Credits

**Emerson Teles — EMERSON TELES:** in-game testing, symptom identification, calibration selection, following validation and organization. Implementation and local verification with Codex assistance. Silent Hill: Homecoming and Unknown Project belong to their respective authors.
