"""Linear controller pitch and post-curve Precision sensitivity scaling."""
from pathlib import Path
import struct,hashlib
from build_navigation_aligned import build as aligned_build,asm,offset,CAVE,HELPER,AIM_SITE,AIM_CAVE,AIM_ORIGINAL
ROOT=Path(__file__).resolve().parent.parent
OUTPUT=ROOT/'build_test/g_SilentHill_camera_response.sgl'
AIM_X,AIM_Y=AIM_CAVE+0xF0,AIM_CAVE+0xF4
AIM_FLAG,AIM_INPUT_REFERENCE=AIM_CAVE+0xF8,AIM_CAVE+0xFC
AIM_OUTPUT_X_SITE,AIM_OUTPUT_Y_SITE=0x10711F24,0x1071EA28
AIM_OUTPUT_X_CAVE,AIM_OUTPUT_Y_CAVE=CAVE+0x400,CAVE+0x480
PITCH_MASK=CAVE+0x2D0
ORIGINAL_OUTPUT_X=bytes.fromhex('F3 0F 10 05 E4 A2 F8 10')
ORIGINAL_OUTPUT_Y=bytes.fromhex('F3 0F 11 44 24 1C')

def build():
    original,code,helper,old_aim=aligned_build()
    image=bytearray(original)
    # Replace squared Y with absolute Y at the controller-only pitch path.
    # XMM0 already holds dt as double; EBX is the verified input-frame pointer.
    pitch=asm(f'''
        cvtss2sd xmm1, dword ptr [ebx+0x24]
        andpd xmm1, xmmword ptr [0x{PITCH_MASK:x}]
        mulsd xmm1, qword ptr [0x10f91290]
        mulsd xmm1, qword ptr [0x{CAVE+0x2f0:x}]
        jmp 0x108db003
    ''',CAVE+0x200)
    assert len(pitch)<=0x40
    pos=offset(CAVE+0x200,0x40);image[pos:pos+0x40]=pitch+b'\xcc'*(0x40-len(pitch))
    image[offset(PITCH_MASK,16):offset(PITCH_MASK,16)+16]=struct.pack('<2Q',0x7fffffffffffffff,0x7fffffffffffffff)
    aim=asm(f'''
        pushfd
        push eax
        push edx
        mov eax, dword ptr [0x{AIM_FLAG:x}]
        test eax, eax
        jz finish
        mov dword ptr [eax], 0
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
        mov eax, dword ptr [eax+0x28c]
        test eax, eax
        jz finish
        add edx, eax
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
        mov edx, dword ptr [0x{AIM_FLAG:x}]
        mov dword ptr [edx], 1
        sub esp, 16
        movups xmmword ptr [esp], xmm0
        movss xmm0, dword ptr [esi+0xae8]
        mulss xmm0, dword ptr [0x{AIM_INPUT_REFERENCE:x}]
        movss dword ptr [esi+0xae8], xmm0
        movss xmm0, dword ptr [esi+0xaec]
        mulss xmm0, dword ptr [0x{AIM_INPUT_REFERENCE:x}]
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
    pos=offset(AIM_CAVE,0xf0);image[pos:pos+0xf0]=aim+b'\xcc'*(0xf0-len(aim))
    image[offset(AIM_FLAG,8):offset(AIM_FLAG,8)+8]=struct.pack('<If',0,2.0)
    assert image[offset(AIM_OUTPUT_X_CAVE,0x100):offset(AIM_OUTPUT_X_CAVE,0x100)+0x100]==b'\xcc'*0x100
    output_x=asm(f'''
        pushfd
        push eax
        mov eax, dword ptr [0x{AIM_FLAG:x}]
        test eax, eax
        je native
        cmp dword ptr [eax], 0
        je native
        movss xmm0, dword ptr [esp+0x28]
        mulss xmm0, dword ptr [0x{AIM_X:x}]
        movss dword ptr [esp+0x28], xmm0
    native:
        pop eax
        popfd
        movss xmm0, dword ptr [0x10f8a2e4]
        jmp 0x{AIM_OUTPUT_X_SITE+8:x}
    ''',AIM_OUTPUT_X_CAVE)
    output_y=asm(f'''
        pushfd
        push eax
        mov eax, dword ptr [0x{AIM_FLAG:x}]
        test eax, eax
        je native
        cmp dword ptr [eax], 0
        je native
        mulss xmm0, dword ptr [0x{AIM_Y:x}]
    native:
        pop eax
        popfd
        movss dword ptr [esp+0x1c], xmm0
        jmp 0x{AIM_OUTPUT_Y_SITE+6:x}
    ''',AIM_OUTPUT_Y_CAVE)
    for site,target,expected,hook in [(AIM_OUTPUT_X_SITE,AIM_OUTPUT_X_CAVE,ORIGINAL_OUTPUT_X,output_x),
                                      (AIM_OUTPUT_Y_SITE,AIM_OUTPUT_Y_CAVE,ORIGINAL_OUTPUT_Y,output_y)]:
        assert len(hook)<0x80
        assert image[offset(site,len(expected)):offset(site,len(expected))+len(expected)]==expected
        image[offset(target,len(hook)):offset(target,len(hook))+len(hook)]=hook
        patch=b'\xe9'+struct.pack('<i',target-site-5)+b'\x90'*(len(expected)-5)
        image[offset(site,len(patch)):offset(site,len(patch))+len(patch)]=patch
    # The user-confirmed normal yaw detour and actor alignment remain identical.
    assert image[offset(CAVE,len(code)):offset(CAVE,len(code))+len(code)]==original[offset(CAVE,len(code)):offset(CAVE,len(code))+len(code)]
    assert image[offset(HELPER,len(helper)):offset(HELPER,len(helper))+len(helper)]==original[offset(HELPER,len(helper)):offset(HELPER,len(helper))+len(helper)]
    return bytes(image),code,helper,aim

if __name__=='__main__':
    image,code,helper,aim=build();OUTPUT.write_bytes(image)
    print(f'sha256={hashlib.sha256(image).hexdigest().upper()}; aim code={len(aim)}')
