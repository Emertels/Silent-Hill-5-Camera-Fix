# 🕹️ Camera Fix Patch 1.0 — Configuration Manual & Technical Reference

<p align="center">
  <a href="MANUAL.md"><img src="https://img.shields.io/badge/Manual-Português%20(PT--BR)-009c3b?style=for-the-badge&logo=readme&logoColor=white" alt="Versão em Português"></a>
  <a href="MANUAL-EN.md"><img src="https://img.shields.io/badge/Manual-English-0052cc?style=for-the-badge&logo=readme&logoColor=white" alt="English Version"></a>
</p>

## Normalized Vertical Reference — Version 1.0, October 12, 2026

Emerson approved horizontal turning at 1.0, aiming at 1.0/2.0, and overall motion at 2.0. In subsequent side-by-side comparisons, he selected the speed of **previous vertical 2.0** as the closest baseline to horizontal 1.0. The new normalization implements this choice: **new VerticalCameraSpeed=1.0 equals the gain of previous 2.0**.

The proxy DLL multiplies only the vertical reference by 2. The base angular factor extracted from the SGL remains 1.432394498923; the effective reference is 2 × 1.432394498923 = **2.864788997846**. The linear vertical curve and native clamp limits remain. Horizontal motion, aiming scaling, character following, SGL code, and bindings remain unchanged.

This is an **empirical calibration chosen by the user**, establishing an exact equivalence between previous and new gains rather than a physical parity measurement. Before limits, maximum requested vertical rate is now 3 × VerticalCameraSpeed rad/s, while horizontal remains 1.5 × HorizontalCameraSpeed. The rates differ by design to achieve balanced feel; they do not represent identical physical degree rates.

On the new vertical scale: 1.0 = previous 2.0; 1.5 = previous 3.0; 2.0 requests the equivalent of previous 4.0, and 3.0 requests previous 6.0. The previous 4/6 gains were not accepted by the previous INI; here they represent internal gain equivalents. The INI continues to accept **0.25 to 3.0**. Speeds at 2.0 and 3.0 are faster vertically than before, so start at the new 1.0 before increasing.

Default vertical is set to 1.0 to test the chosen reference. Personal INI values are preserved. The public package includes four 1.0 defaults. Game launch and stability were validated; in-game perception of this normalized baseline was approved. Aiming scaling remains identical.

Previous backup: `C:\Projetos\SilentHill5-CameraFix\_backup\antes_normalizar_vertical_v1_20261012_125613`. The x86 build, factor/normalization verification, and native regression tests using `PAGE_EXECUTE_READ` passed. The Precision state flag resides in writable DLL memory. Public release remains 1.0.

**Updated on October 12, 2026 • Emerson Teles — EMERSON TELES**

This manual covers installation, four sensitivity adjustments, accepted ranges, percentages, calibration, legacy options, and restoration. Developed and tested on the Unknown Project 3.20 installation. Other builds or unmodded installations have not been validated.

---

## 1. Current Status

The game launches stably following the Precision flag memory relocation. Emerson validated character-following camera, horizontal turning at 1.0/2.0, aiming at 1.0/2.0, and testing with all settings at 2.0. Subsequent feedback selected previous vertical 2.0 as the new baseline 1.0. The DLL was normalized to this equivalence.

The package ships with four 1.0 defaults. Your installed INI may contain personalized values. During this documentation update, no binaries, bindings, or calculations were altered.

---

## 2. Where to Configure

After installation, edit **Bin/camera_axis_fix.ini** inside your game folder. The INI in `Files/Bin` belongs to the installation package: editing that copy does not affect the game until copied to `Bin`.

Procedure:
1. Close the game and open the installed INI in a text editor (Notepad, VS Code, etc.).
2. In the `[Camera]` section, edit the desired number using a decimal dot (`.`).
3. Save the file keeping the name `camera_axis_fix.ini` (not `.ini.txt`), and restart the game.

Options are parsed during game initialization. Saving while the game is running does not update sensitivities in the active session.

```ini
[Camera]
HorizontalCameraSpeed=1.0
VerticalCameraSpeed=1.0
AimHorizontalSpeed=1.0
AimVerticalSpeed=1.0
```

Keep one line per option. Avoid duplicate keys. Place comments on their own lines starting with `;`.

---

## 3. What Each Setting Does

**HorizontalCameraSpeed:** Left/right turning of the normal camera using the right analog stick. Also governs character rotation to track camera direction. Does not increase walking or running speeds from the left stick. The approved character-following routine derives camera angles from the character's actual heading after turning.

**VerticalCameraSpeed:** Up/down motion of the normal camera. The controller path uses a linear curve and an angular factor derived from native vertical constants. Remains subject to native deadzones and pitch clamping limits. Does not enable unlimited vertical rotation.

**AimHorizontalSpeed:** Left/right aiming sensitivity when holding weapons in Precision camera mode. Applied after the native curve output. Does not modify HorizontalCameraSpeed.

**AimVerticalSpeed:** Up/down aiming sensitivity in Precision camera mode. Does not modify VerticalCameraSpeed.

You can set distinct values for each of the four settings. For instance, normal horizontal = 1.0, normal vertical = 1.2, and aiming X/Y = 1.0 operate independently. To evaluate balance, keep horizontal fixed while tuning vertical.

---

## 4. Accepted Values and Range

There is no rigid list of fixed steps. All four options accept **decimals from 0.25 to 3.0**, including boundaries and arbitrary intermediates: 1.01, 1.1, 1.15, 1.2, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, etc. Floating-point precision matches the underlying C implementation.

Use `1.2`, not `1,2`. Integers such as `1`, `2`, and `3` are valid, though `1.0` formatting is recommended.

Parser rules:
- Valid value within 0.25..3.0: applied directly.
- Numeric value below 0.25 (e.g., 0 or 0.1): clamped to 0.25. Zero **does not** disable the mod.
- Numeric value above 3.0 (e.g., 4.0 or 5.0): clamped to 3.0.
- Missing value or invalid text: falls back to default 1.0. Do not use negative signs, commas, scientific notation (`1e0`), or suffix units (`1.2x`).
- Excessively large numbers may trigger the parser fallback to 1.0 rather than clamping. For predictable results, stay within 0.25 to 3.0.

The log records multipliers rounded to two decimal places. This does not mean the parser truncates precision: values like 1.125 are utilized with full float precision even if logged with two decimals.

---

## 5. Percentages Relative to 1.0

Formula: **Reference percentage = value × 100**. Increase or decrease relative to 1.0: **(value − 1) × 100**.

- `0.25`: 25% of baseline (−75% reduction).
- `0.50`: 50% of baseline (−50% reduction).
- `0.75`: 75% of baseline (−25% reduction).
- `1.00`: 100%, the calibrated default baseline.
- `1.10`: 110% (+10% gain).
- `1.15`: 115% (+15% gain).
- `1.20`: 120% (+20% gain).
- `1.25`: 125% (+25% gain).
- `1.50`: 150% (+50% gain).
- `1.75`: 175% (+75% gain).
- `2.00`: 200% (+100% gain, double baseline).
- `2.25`: 225% (+125% gain).
- `2.50`: 250% (+150% gain).
- `2.75`: 275% (+175% gain).
- `3.00`: 300% (+200% gain, triple baseline).

These percentages define **calculation multipliers**, not absolute visible screen rotation speeds. Acceleration, bounds, framing, and collisions influence final motion.

To compare two non-default values, use **(new ÷ previous − 1) × 100**. Moving from 1.1 to 1.2 is a ~9.09% increase, even though 1.2 is +20% over 1.0. Moving from 2.0 to 2.5 is a +25% increase, not +50%.

---

## 6. Normal Camera Calculation & Vertical Reference

Horizontal requested speed at full stick deflection is `1.5 × HorizontalCameraSpeed` rad/s before body rotation clamping. At 1.0, reference speed is ~85.94 degrees/s; at 2.0, 171.89; at 3.0, 257.83. Partial stick tilt scales input linearly.

Original game vertical controller code references 60 degrees/s. Native radian conversion factor is 0.01745329238474369. Base gain calculated from native SGL constants is:

```text
Vertical Gain = 1.5 / (60 × 0.01745329238474369)
              = 1.432394498923
```

The vertical path eliminates squared controller input and uses its absolute value (`ANDPD`). The current normalization adds an empirical factor of 2 chosen by Emerson Teles: effective vertical gain = **2.864788997846 × setting**. Y1.0 matches previous Y2.0. This calibrates vertical speed to match user feel rather than enforced mathematical equality.

The vertical axis retains native pitch limits, deadzones, and framing collision. **Do not assume identical physical rates across all degrees of rotation.** The 1.0 setting is the mod's calibrated standard.

---

## 7. Aiming Reference (Precision Camera)

Aiming speed applies **INI value ÷ 3.0** after native curve calculations, preserving a stable baseline:

- Aim 1.0: one third of previous prototype reference.
- Aim 1.5: one half of that reference.
- Aim 2.0: two thirds of that reference.
- Aim 2.5: five sixths (~83.33%).
- Aim 3.0: full speed of the earlier prototype baseline.

Relative to the **current** 1.0 baseline, aim 2.0 applies double the multiplier and aim 3.0 applies triple.

Post-curve scaling ensures that increasing the INI value does not inflate the quadratic acceleration effect. User testing confirmed aim at 1.0 and 2.0 provides excellent precision.

---

## 8. Calibration Guidance

1. Start with `HorizontalCameraSpeed=1.0` and `VerticalCameraSpeed=1.0`.
2. Test `VerticalCameraSpeed=1.1` without changing horizontal or aiming simultaneously.
3. If still slow, test 1.2; if too sensitive, try 1.15.
4. Restart between changes. Compare in the same room with identical stick deflections.
5. Once comfortable, verify walking vs standing turning and extreme stick tilt.

One recommended user setup is setting all four values to 2.0. Another preferred setup is aiming at 1.0 and camera at 1.0 or 1.2. Choose what fits your personal playstyle.

---

## 9. Practical Tips

- Change **one option at a time** to clearly observe its effect.
- For fine adjustments, use steps of 0.05 or 0.1. For broader testing, 1.0, 1.5, and 2.0 are distinct baselines.
- Test both slight and full stick deflection. Deadzones can feel like sluggishness without affecting maximum speed.
- Test in open areas away from walls to prevent camera collision interference.
- The vertical camera stops at native pitch limits; hitting limits does not mean sensitivity stopped working.
- Do not adjust mouse or left-stick settings to compensate for this fix.
- Keep the CFG files' right-stick multipliers at 1.0 so INI options remain meaningful.
- Back up your tuned INI before reinstalling packages.
- Always use the matching SGL and DLL from the same release.

---

## 10. Legacy Options & Compatibility Fields

The INI retains legacy fields parsed by the base input DLL. They are not primary speed controls for the modded camera:

```ini
RightStickXExponent=1.0
RightStickYExponent=1.0
RightStickXGain=1.0
RightStickYGain=1.0
```

- **RightStickXExponent / RightStickYExponent = 1.0:** Maintains neutral input curvature before mod calculations.
- **RightStickXGain / RightStickYGain = 1.0:** Prevents duplicate input gain stacking.

The documented range (0.25..3.0) applies strictly to the **four main speed settings**, not legacy fields.

---

## 11. CFG File Bindings & Installation

The files `Engine/binds_pc_mjs.cfg` and `Engine/bindcfgs_pc.cfg` remain required to bind gamepad inputs. In this setup, both are configured with:

```text
setbind 1 COMMAND_CAMERA_X CONTROLLER 0 AXIS_RX -1.0 1.0 1.0
setbind 1 COMMAND_CAMERA_Y CONTROLLER 0 AXIS_RY -1.0 1.0 1.0
setbind 1 COMMAND_TURNLEFT DEVICE_INVALID 0 0
setbind 1 COMMAND_TURNRIGHT DEVICE_INVALID 0 0
```

Preserve keyboard `addbind` entries and other commands. Because the mod turns the character body together with the camera, right-stick `TURNLEFT` and `TURNRIGHT` must be set to `DEVICE_INVALID` to avoid duplicate turns.

Installation steps:
1. Close the game and back up your `Bin` files and both CFGs.
2. Copy all **four files** from `Files/Bin` into the game's `Bin` folder.
3. Verify the bindings above in both CFGs.
4. Launch the game and play.

Package files: `g_SilentHill.sgl`, `xinput1_3.dll`, `camera_input_base.dll`, and `camera_axis_fix.ini`.

---

## 12. Logs & Troubleshooting

The mod generates `Bin/camera_axis_fix.log`:
- `Navigation speed: ...; applied`: confirms normal camera settings applied.
- `Precision speed: ...; post-curve scale=value/3; applied`: confirms aiming scale applied.
- `rejected`: indicates signature mismatch or memory protection error.

If changes do not take effect, verify you edited the INI in the active `Bin` folder, saved with decimal dots, and restarted the game.

The pre-menu crash from earlier versions was traced to memory writes inside write-protected executable pages (`0xC0000005`). Moving the state flag to writable DLL data completely resolved the issue.

---

## 13. Restoring the Original Game

To uninstall the mod and revert to the baseline state:

1. Close the game.
2. Copy `Files/_Backup Original/Bin/g_SilentHill.sgl` into your game's `Bin` directory, overwriting the modified file.
3. Remove the mod's auxiliary files from `Bin`:
   - `camera_axis_fix.ini`
   - `camera_input_base.dll`
   - `xinput1_3.dll`
4. Restore your personal CFG backups if you modified bindings.

Official GitHub repository: https://github.com/Emertels/Silent-Hill-5-Camera-Fix

---

## Credits

**Emerson Teles (EMERSON TELES):** Testing, symptom identification, vertical and aiming calibration, package organization, and validation. Implementation and verification with Codex assistance. *Silent Hill: Homecoming* and *Unknown Project* belong to their respective copyright holders.
