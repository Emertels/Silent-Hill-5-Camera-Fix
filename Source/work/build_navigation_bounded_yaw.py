"""Experimental bounded manual yaw; native following resumes at neutral input."""
import hashlib
import json
import math
import struct
from pathlib import Path
import build_navigation_native_yaw as original
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

CAVE,SITE,RATE,offset=original.CAVE,original.SITE,original.RATE,original.offset
LIMIT=math.radians(80)
DEADZONE=0.05
SOURCE=str(Path(original.SOURCE).parent/'_backup'/'before_navigation_native_yaw_20261011_012117'/'g_SilentHill.sgl')
cleanup_plan=Path(__file__).resolve().parent/'manual_camera_cleanup_plan.json'
if not Path(SOURCE).exists() and cleanup_plan.exists():
    archive=Path(json.loads(cleanup_plan.read_text(encoding='utf-8'))['archive'])
    SOURCE=str(archive/'Bin'/'_backup'/'before_navigation_native_yaw_20261011_012117'/'g_SilentHill.sgl')
OUTPUT=str(Path(original.OUTPUT).with_name('g_SilentHill_navigation_bounded_yaw.sgl'))

def build(source):
    assert hashlib.sha256(source).hexdigest().upper()==original.EXPECTED_HASH
    site=offset(SITE,6); cave=offset(CAVE,0x100)
    assert source[site:site+6]==original.ORIGINAL
    assert source[cave:cave+0x100]==b'\xcc'*0x100
    constants=[RATE,math.pi,2*math.pi,LIMIT,-LIMIT,DEADZONE*DEADZONE]
    pushes='\n'.join('push 0x%08x'%struct.unpack('<I',struct.pack('<f',v))[0] for v in constants)
    asm=f'''
        pushfd
        push eax
        sub esp, 32
        movups xmmword ptr [esp], xmm1
        movups xmmword ptr [esp+16], xmm2
        {pushes}
        mov eax, dword ptr [ebp+0xc]
        movss xmm1, dword ptr [eax+0x20]
        movaps xmm2, xmm1
        mulss xmm2, xmm2
        comiss xmm2, dword ptr [esp]
        jbe finish
        movss xmm0, dword ptr [esi+0x11c]
        mulss xmm1, dword ptr [esp+0x64]
        mulss xmm1, dword ptr [esp+0x14]
        subss xmm0, xmm1
        subss xmm0, xmm5
    wrap_high:
        comiss xmm0, dword ptr [esp+0x10]
        jbe wrap_low_start
        subss xmm0, dword ptr [esp+0xc]
        jmp wrap_high
    wrap_low_start:
        xorps xmm2, xmm2
        subss xmm2, dword ptr [esp+0x10]
    wrap_low:
        comiss xmm0, xmm2
        jae clamp_angle
        addss xmm0, dword ptr [esp+0xc]
        jmp wrap_low
    clamp_angle:
        maxss xmm0, dword ptr [esp+4]
        minss xmm0, dword ptr [esp+8]
        addss xmm0, xmm5
        mov dword ptr [esi+0x120], 0
    finish:
        add esp, 24
        movups xmm1, xmmword ptr [esp]
        movups xmm2, xmmword ptr [esp+16]
        add esp, 32
        pop eax
        popfd
        movss dword ptr [esp+0x28], xmm0
        jmp 0x{SITE+6:x}
    '''
    machine,_=Ks(KS_ARCH_X86,KS_MODE_32).asm(asm,CAVE)
    code=bytes(machine)
    assert len(code)<=0x100,len(code)
    image=bytearray(source)
    image[site:site+6]=b'\xe9'+struct.pack('<i',CAVE-SITE-5)+b'\x90'
    image[cave:cave+len(code)]=code
    return bytes(image),code

if __name__=='__main__':
    image,code=build(Path(SOURCE).read_bytes())
    Path(OUTPUT).write_bytes(image)
    print('output='+OUTPUT)
    print('sha256='+hashlib.sha256(image).hexdigest().upper())
    print('code_bytes='+str(len(code)))
