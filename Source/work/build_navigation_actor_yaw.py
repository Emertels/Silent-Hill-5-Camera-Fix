"""Bounded Navigation yaw plus native player rotation, experimental."""
import hashlib
import struct
from pathlib import Path
import build_navigation_bounded_yaw as bounded
from keystone import Ks,KS_ARCH_X86,KS_MODE_32

CAVE,SITE,RATE,LIMIT,DEADZONE,SOURCE,offset=(bounded.CAVE,bounded.SITE,bounded.RATE,
    bounded.LIMIT,bounded.DEADZONE,bounded.SOURCE,bounded.offset)
HELPER=CAVE+0x100
ROTATE=0x10145F50
OUTPUT=str(Path(bounded.OUTPUT).with_name('g_SilentHill_navigation_actor_yaw.sgl'))

def build(source):
    image,code=bounded.build(source)
    assert source[offset(HELPER,0x100):offset(HELPER,0x100)+0x100]==b'\xcc'*0x100
    assert source[offset(ROTATE,12):offset(ROTATE,12)+12]==bytes.fromhex('55 8B EC 83 E4 F0 83 EC 30 0F 57 C0')
    marker=bytes.fromhex('C7 86 20 01 00 00 00 00 00 00')
    assert code.count(marker)==1
    # Insert a relative call immediately after clearing follower velocity.
    pos=code.index(marker)+len(marker)
    # All branches in bounded's first trampoline must be reassembled because
    # insertion changes jump destinations. Use a same-size out-of-line detour
    # for the original 10-byte velocity store instead.
    start=code.index(marker)
    jump=b'\xe9'+struct.pack('<i',HELPER-(CAVE+start)-5)+b'\x90'*5
    code=code[:start]+jump+code[start+len(marker):]
    ret=CAVE+pos
    degrees=struct.unpack('<I',struct.pack('<f',-57.295780181884766))[0]
    # EDI is the player's transform (entity+0x1A0) at this exact site; XMM1
    # holds X*dt*RATE in radians. Native cdecl rotation expects degrees.
    # Save all integer, SSE and x87 state across the engine call, including
    # the live x87 pitch value required after the hook. Use aligned FXSAVE.
    asm=f'''
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
        fxrstor [esp]
        mov esp, ebx
        popad
        popfd
        jmp 0x{ret:x}
    '''
    machine,_=Ks(KS_ARCH_X86,KS_MODE_32).asm(asm,HELPER)
    helper=bytes(machine)
    assert len(helper)<=0x100,len(helper)
    image=bytearray(image)
    p=offset(CAVE,len(code));image[p:p+len(code)]=code
    p=offset(HELPER,len(helper));image[p:p+len(helper)]=helper
    return bytes(image),code,helper

if __name__=='__main__':
    image,code,helper=build(Path(SOURCE).read_bytes())
    Path(OUTPUT).write_bytes(image)
    print('output='+OUTPUT)
    print('sha256='+hashlib.sha256(image).hexdigest().upper())
    print('helper_bytes='+str(len(helper)))
