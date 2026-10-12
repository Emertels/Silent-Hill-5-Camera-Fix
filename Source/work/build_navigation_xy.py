"""Add Navigation-only vertical gain to the gameplay-confirmed camera SGL."""
import hashlib
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'pydeps'))
from keystone import KS_ARCH_X86, KS_MODE_32, Ks
from build_navigation_bounded_yaw import offset

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / '_backup' / 'camera_fix_confirmado_antes_xy_ini_20261011' / 'g_SilentHill.sgl'
SOURCE_SHA256 = "BB733561706B00181FDEE054D42B3920F37DF1F268A14408A1E415AE05AB267A"
OUTPUT = ROOT / "build_test" / "g_SilentHill_navigation_xy.sgl"
CAVE = 0x10386200
SITE_A, SITE_B = 0x108DAFFB, 0x108DB012
ORIGINAL_A = bytes.fromhex("f20f590d9012f910")
ORIGINAL_B = bytes.fromhex("f30f100d68631d11")
VERTICAL_DOUBLE, VERTICAL_FLOAT = CAVE + 0xF0, CAVE + 0xF8


def assemble(asm, address):
    encoded, _ = Ks(KS_ARCH_X86, KS_MODE_32).asm(asm, address)
    return bytes(encoded)


def patch(source):
    if hashlib.sha256(source).hexdigest().upper() != SOURCE_SHA256:
        raise ValueError("SGL differs from gameplay-confirmed camera correction")
    result = bytearray(source)
    if result[offset(CAVE, 0x100):offset(CAVE, 0x100)+0x100] != b"\xcc"*0x100:
        raise ValueError("Vertical code cave occupied")
    for site, original in ((SITE_A, ORIGINAL_A), (SITE_B, ORIGINAL_B)):
        if result[offset(site, 8):offset(site, 8)+8] != original:
            raise ValueError(f"Navigation pitch signature differs at {site:x}")

    first = assemble(f"""
        mulsd xmm1, qword ptr [0x10f91290]
        mulsd xmm1, qword ptr [0x{VERTICAL_DOUBLE:x}]
        jmp 0x{SITE_A+8:x}
    """, CAVE)
    second = assemble(f"""
        movss xmm1, dword ptr [0x111d6368]
        mulss xmm1, dword ptr [0x{VERTICAL_FLOAT:x}]
        jmp 0x{SITE_B+8:x}
    """, CAVE+0x40)
    if len(first) > 0x40 or len(second) > 0xB0:
        raise ValueError("Vertical detour too large")
    result[offset(CAVE, len(first)):offset(CAVE, len(first))+len(first)] = first
    result[offset(CAVE+0x40, len(second)):offset(CAVE+0x40, len(second))+len(second)] = second
    result[offset(VERTICAL_DOUBLE, 8):offset(VERTICAL_DOUBLE, 8)+8] = struct.pack('<d', 1.0)
    result[offset(VERTICAL_FLOAT, 4):offset(VERTICAL_FLOAT, 4)+4] = struct.pack('<f', 1.0)
    for site, target in ((SITE_A, CAVE), (SITE_B, CAVE+0x40)):
        detour = b'\xe9' + struct.pack('<i', target-site-5) + b'\x90'*3
        result[offset(site, 8):offset(site, 8)+8] = detour
    return bytes(result)


if __name__ == '__main__':
    output = patch(SOURCE.read_bytes())
    OUTPUT.write_bytes(output)
    print(f"output={OUTPUT}\nsha256={hashlib.sha256(output).hexdigest().upper()}")
