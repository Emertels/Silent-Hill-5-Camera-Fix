"""Experimental native horizontal integration in TCamComNavigationSHV only."""
import hashlib
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
from trace_camera import sections
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = r"F:\Jogos\Silent Hill (TUDO)\Silent Hill 5 - Homecoming\Silent Hill 5 - Homecoming (Update 3.20)(PT-BR) - [PC]-By Emerson Teles\Bin\g_SilentHill.sgl"
OUTPUT = os.path.join(ROOT, "build_test", "g_SilentHill_navigation_native_yaw.sgl")
EXPECTED_HASH = "352264681F88B6A5F29C0581B32CE4A274F0E839B9F517ACF48701B35371E474"
SITE = 0x108DB3D6
CAVE = 0x10386000
ORIGINAL = bytes.fromhex("F3 0F 11 44 24 28")
RATE = 2.2  # radians per second at full deflection, approximately 126 deg/s.

def offset(va, size):
    for _, start, raw, length in sections:
        if start <= va and va + size <= start + length:
            return raw + va - start
    raise ValueError(hex(va))

def build(source):
    if hashlib.sha256(source).hexdigest().upper() != EXPECTED_HASH:
        raise ValueError("Source is not the verified pre-experiment SGL")
    site = offset(SITE, len(ORIGINAL))
    cave = offset(CAVE, 0x100)
    if source[site:site + len(ORIGINAL)] != ORIGINAL:
        raise ValueError("Navigation angle store signature mismatch")
    if source[cave:cave + 0x100] != b"\xcc" * 0x100:
        raise ValueError("Code cave is not unused INT3 padding")
    # Arguments for the component update are verified statically: EBP+0xC
    # is its camera-control frame, X at +0x20. ESP+0x24 is frame elapsed time.
    # Preserve EAX, EFLAGS, and all of XMM1. XMM0 replaces the original yaw
    # result and is stored by the original instructions immediately after.
    rate_bits = struct.unpack("<I", struct.pack("<f", RATE))[0]
    assembly = f"""
        pushfd
        push eax
        sub esp, 16
        movups xmmword ptr [esp], xmm1
        mov eax, dword ptr [ebp + 0xc]
        movss xmm0, dword ptr [esi + 0x11c]
        movss xmm1, dword ptr [eax + 0x20]
        mulss xmm1, dword ptr [esp + 0x3c]
        push 0x{rate_bits:08x}
        mulss xmm1, dword ptr [esp]
        add esp, 4
        subss xmm0, xmm1
        movups xmm1, xmmword ptr [esp]
        add esp, 16
        pop eax
        popfd
        movss dword ptr [esp + 0x28], xmm0
        jmp 0x{SITE + len(ORIGINAL):08x}
    """
    machine, _ = Ks(KS_ARCH_X86, KS_MODE_32).asm(assembly, CAVE)
    trampoline = bytes(machine)
    if len(trampoline) > 0x100:
        raise ValueError("Code cave capacity exceeded")
    result = bytearray(source)
    result[site:site + len(ORIGINAL)] = b"\xe9" + struct.pack("<i", CAVE - SITE - 5) + b"\x90"
    result[cave:cave + len(trampoline)] = trampoline
    return bytes(result), trampoline

if __name__ == "__main__":
    source = open(SOURCE, "rb").read()
    result, trampoline = build(source)
    open(OUTPUT, "wb").write(result)
    print("output=" + OUTPUT)
    print("sha256=" + hashlib.sha256(result).hexdigest().upper())
    print(f"site=0x{SITE:X}; cave=0x{CAVE:X}; size={len(trampoline)}; rate={RATE} rad/s")
