# Camera Fix 1.0 — Source

Mod by Emerson Teles. These are the actual mod sources, generated signature/calibration headers, historical SGL builders and regression tests. No game binary is included in Source.

## Build the current wrapper

Use Windows and GCC with 32-bit code generation, dlltool and as.  From this Source folder run:

```powershell
.\work\build_wrapper.ps1 -CompilerDirectory 'C:\path\to\gcc\bin'
```

The script uses the supplied current headers, builds build_test/xinput1_3_configurable.dll and build_test/camera_input_base.dll and runs both native x86 smoke tests. The main input source is src/camera_input_base.c. The release name is xinput1_3.dll. Keep the preserved camera_input_base.dll. The C++ proxy source is also included; rebuilding it requires an x86 Windows C++ toolchain and its export definition. Rebuilt binaries need gameplay testing before replacing a working release.

## SGL generators

The Python files are the development sources, preserved with their original path assumptions. They are not a portable one-click release builder. They refer to compatible original/intermediate SGL backups and local project paths. Install requirements.txt, review SOURCE/OUTPUT paths and supply the exact compatible images before using them. Do not execute historical builders directly against the installed game. The current wrapper can be compiled without rerunning these generators. Original game code and original backups must not be committed to GitHub.
