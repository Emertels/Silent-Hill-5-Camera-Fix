"""Navigation follows the actual actor heading; Precision input gets own gains."""
from pathlib import Path
import struct
import hashlib
import sys
sys.path.insert(0,str(Path(__file__).parent/'pydeps'))
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from build_navigation_xy import patch,SOURCE,offset
from build_navigation_actor_yaw import build as actor_build,SOURCE as ACTOR_SOURCE,CAVE,HELPER,ROTATE

ROOT=Path(__file__).resolve().parent.parent
OUTPUT=ROOT/'build_test'/'g_SilentHill_navigation_aligned.sgl'
AIM_SITE=0x103851E0
AIM_CAVE=0x10386300
AIM_X,AIM_Y=AIM_CAVE+0xF0,AIM_CAVE+0xF4
AIM_ORIGINAL=bytes.fromhex('F3 0F 10 8E D8 0A 00 00')

def asm(text,address):return bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(text,address)[0])

def build():
    image=bytearray(patch(SOURCE.read_bytes()))
    _,code,old_helper=actor_build(Path(ACTOR_SOURCE).read_bytes())
    marker=bytes.fromhex('C7 86 20 01 00 00 00 00 00 00')
    # The old helper returns immediately after the replaced velocity clear.
    # Its final E9 contains the reliable return address in the code cave.
    ret=HELPER+len(old_helper)+struct.unpack('<i',old_helper[-4:])[0]
    degrees=struct.unpack('<I',struct.pack('<f',-57.295780181884766))[0]
    helper=asm(f'''
        mov dword ptr [esi+0x120], 0
        pushfd
        pushad
        mov ebx, esp
        sub esp, 0x210
        and esp, 0xfffffff0
        fxsave [esp]
        fninit
        push 0x{degrees:08x}
        mulss xmm1, dword ptr [esp]
        movss dword ptr [esp], xmm1
        lea eax, [edi-0x1a0]
        push eax
        call 0x{ROTATE:x}
        add esp, 8
        movq xmm0, qword ptr [edi+0x20]
        movq qword ptr [edi+0x440], xmm0
        movq xmm0, qword ptr [edi+0x28]
        movq qword ptr [edi+0x448], xmm0
        fninit
        fld dword ptr [edi+0x28]
        fld dword ptr [edi+0x20]
        call 0x10d20a56
        fstp dword ptr [esp+0x200]
        movss xmm0, dword ptr [esp+0x200]
        xorps xmm1, xmm1
        comiss xmm0, xmm1
        jae normalized
        cvtss2sd xmm0, xmm0
        addsd xmm0, qword ptr [0x10f91230]
        cvtsd2ss xmm0, xmm0
    normalized:
        movss dword ptr [esi+0x11c], xmm0
        fxrstor [esp]
        movss xmm0, dword ptr [esi+0x11c]
        mov esp, ebx
        popad
        popfd
        jmp 0x{ret:x}
    ''',HELPER)
    assert len(helper)<0x100
    pos=offset(HELPER,0x100)
    image[pos:pos+0x100]=helper+b'\xcc'*(0x100-len(helper))
    # Actor input's +AE8/+AEC path was shown by gameplay to affect weapon aim.
    # Guard it with the active camera name; other camera modes remain native.
    assert image[offset(AIM_SITE,8):offset(AIM_SITE,8)+8]==AIM_ORIGINAL
    assert image[offset(AIM_CAVE,0x100):offset(AIM_CAVE,0x100)+0x100]==b'\xcc'*0x100
    aim=asm(f'''
        pushfd
        push eax
        push edx
        mov eax, dword ptr [0x1158982c]
        test eax, eax
        jz finish
        mov eax, dword ptr [eax+8]
        test eax, eax
        jz finish
        mov edx, dword ptr [eax+0x288]
        test edx, edx
        jz empty
        cmp edx, 256
        ja finish
        imul edx, edx, 0x60
        add edx, dword ptr [eax+0x28c]
        mov eax, dword ptr [edx-0x5c]
        jmp camera
    empty:
        mov eax, dword ptr [eax+0x2b0]
    camera:
        test eax, eax
        jz finish
        mov eax, dword ptr [eax+0x248]
        test eax, eax
        jz finish
        cmp dword ptr [eax], 0x63657250
        jne finish
        cmp dword ptr [eax+4], 0x6f697369
        jne finish
        cmp word ptr [eax+8], 0x006e
        jne finish
        sub esp, 16
        movups xmmword ptr [esp], xmm0
        movss xmm0, dword ptr [esi+0xae8]
        mulss xmm0, dword ptr [0x{AIM_X:x}]
        movss dword ptr [esi+0xae8], xmm0
        movss xmm0, dword ptr [esi+0xaec]
        mulss xmm0, dword ptr [0x{AIM_Y:x}]
        movss dword ptr [esi+0xaec], xmm0
        movups xmm0, xmmword ptr [esp]
        add esp, 16
    finish:
        pop edx
        pop eax
        popfd
        movss xmm1, dword ptr [esi+0xad8]
        jmp 0x{AIM_SITE+8:x}
    ''',AIM_CAVE)
    assert len(aim)<0xf0,len(aim)
    image[offset(AIM_CAVE,len(aim)):offset(AIM_CAVE,len(aim))+len(aim)]=aim
    image[offset(AIM_X,8):offset(AIM_X,8)+8]=struct.pack('<2f',1,1)
    image[offset(AIM_SITE,8):offset(AIM_SITE,8)+8]=b'\xe9'+struct.pack('<i',AIM_CAVE-AIM_SITE-5)+b'\x90'*3
    return bytes(image),code,helper,aim

if __name__=='__main__':
    image,code,helper,aim=build()
    OUTPUT.write_bytes(image)
    print(f'sha256={hashlib.sha256(image).hexdigest().upper()}; helper={len(helper)}; aim={len(aim)}')
