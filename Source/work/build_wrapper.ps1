param([Parameter(Mandatory=$true)][string]$CompilerDirectory)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    $gccRoot = $CompilerDirectory
    & (Join-Path $gccRoot 'dlltool.exe') -m i386 -k -d .\work\kernel32_x86.def -l .\build_test\kernel32_x86.a -S (Join-Path $gccRoot 'as.exe') -f '--32'
    if ($LASTEXITCODE) { throw 'Falha ao gerar biblioteca de importaÃ§Ã£o x86' }
    & (Join-Path $gccRoot 'gcc.exe') -m32 -shared -nostdlib -fno-builtin -fno-stack-protector -O2 -I. -I.\src .\src\camera_speed_wrapper.c .\work\camera_speed_wrapper.def .\build_test\kernel32_x86.a '-Wl,--entry,_DllMain@12' '-Wl,--no-insert-timestamp' -o .\build_test\xinput1_3_configurable.dll
    if ($LASTEXITCODE) { throw 'Falha ao compilar wrapper' }
    & (Join-Path $gccRoot 'gcc.exe') -m32 -msse2 -mfpmath=sse -shared -nostdlib -fno-builtin -fno-stack-protector -O2 .\src\camera_input_base.c .\work\camera_speed_wrapper.def .\build_test\kernel32_x86.a '-Wl,--entry,_DllMain@12' '-Wl,--no-insert-timestamp' -o .\build_test\camera_input_base.dll
    if ($LASTEXITCODE) { throw 'Failed to build native input base' }
    & (Join-Path $gccRoot 'gcc.exe') -m32 -nostdlib -fno-builtin -fno-stack-protector -O2 -I. -I.\src .\build_test\navigation_speed_smoke.c .\build_test\kernel32_x86.a '-Wl,--entry,_start@0' -o .\build_test\navigation_speed_smoke.exe
    if ($LASTEXITCODE) { throw 'Falha ao compilar teste' }
    & .\build_test\navigation_speed_smoke.exe
    if ($LASTEXITCODE) { throw "Teste falhou: $LASTEXITCODE" }
    'PASS: configurable speed x86 smoke'
    & (Join-Path $gccRoot 'gcc.exe') -m32 -msse2 -nostdlib -fno-builtin -fno-stack-protector -O2 -I. -I.\src .\build_test\camera_protection_smoke.c .\build_test\kernel32_x86.a '-Wl,--entry,_start@0' -o .\build_test\camera_protection_smoke.exe
    if ($LASTEXITCODE) { throw 'Falha ao compilar teste de proteÃ§Ã£o real' }
    & .\build_test\camera_protection_smoke.exe
    if ($LASTEXITCODE) { throw "Teste de proteÃ§Ã£o real falhou: $LASTEXITCODE" }
    'PASS: actual x86 detour with READ/EXECUTE code and writable DLL state'
} finally { Pop-Location }


