"""Exercise sustained heading alignment and Precision-only input gain."""
import sys,struct,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'pydeps'))
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
from build_navigation_response import build,AIM_SITE,AIM_CAVE,AIM_X,AIM_Y,AIM_INPUT_REFERENCE,AIM_FLAG
from build_navigation_actor_yaw import CAVE,HELPER,SITE,ROTATE,offset
image,code,helper,aim=build()
def f(x):return struct.pack('<f',x)
def u(x):return struct.pack('<I',x)
def readf(uc,a):return struct.unpack('<f',uc.mem_read(a,4))[0]
def readu(uc,a):return struct.unpack('<I',uc.mem_read(a,4))[0]
def angle_delta(a,b):return (a-b+math.pi)%(2*math.pi)-math.pi

def run(rate,x,fps,heading):
    uc=Uc(UC_ARCH_X86,UC_MODE_32)
    for a,n in [(0x108db000,0x1000),(CAVE,0x1000),(0x10145000,0x1000),
                (0x10d20000,0x1000),(0x10f91000,0x1000),(0x200000,0x1000),
                (0x300000,0x1000),(0x400000,0x5000),(0x500000,0x2000)]:uc.mem_map(a,n)
    uc.mem_write(SITE,image[offset(SITE,14):offset(SITE,14)+14])
    uc.mem_write(CAVE,code);uc.mem_write(CAVE+15,f(rate));uc.mem_write(HELPER,helper)
    uc.mem_write(ROTATE,b'\xc3')
    uc.mem_write(0x10d20a56,b'\xd9\xf3\xc3') # FPATAN math stub
    uc.mem_write(0x10f91230,struct.pack('<d',2*math.pi))
    esp,ebp,obj,control,actor=0x402000,0x403000,0x200000,0x300000,0x500000
    uc.mem_write(ebp+12,u(control));uc.mem_write(control+0x20,f(x))
    uc.mem_write(esp+0x24,f(1/fps))
    current=[heading]
    def rotate(machine,address,size,_):
        if address!=ROTATE:return
        stack=machine.reg_read(UC_X86_REG_ESP)
        assert readu(machine,stack+4)==actor
        degree=readf(machine,stack+8)
        assert math.isclose(degree,-x*rate/fps*180/math.pi,abs_tol=1e-4)
        # Simulate additional/native body motion and imperfect actuator response.
        current[0]+=math.radians(degree)*0.85
        machine.mem_write(actor+0x1c0,struct.pack('<4f',math.sin(current[0]),0,math.cos(current[0]),0))
        machine.reg_write(UC_X86_REG_XMM0,0)
    uc.hook_add(UC_HOOK_CODE,rotate)
    sentinel1=0x1234567890abcdef0011223344556677
    sentinel2=0x778899aabbccddeeff00112233445566
    for frame in range(300):
        current[0]+=0.0003 # engine turn drift must not accumulate camera offset
        uc.mem_write(actor+0x1c0,struct.pack('<4f',math.sin(current[0]),0,math.cos(current[0]),0))
        target=math.atan2(math.cos(current[0]),math.sin(current[0]))%(2*math.pi)
        uc.mem_write(obj+0x11c,f(target+0.4 if frame==0 else readf(uc,obj+0x11c)))
        for reg,value in [(UC_X86_REG_ESP,esp),(UC_X86_REG_EBP,ebp),(UC_X86_REG_ESI,obj),
                          (UC_X86_REG_EDI,actor+0x1a0),(UC_X86_REG_EAX,0x12345678),
                          (UC_X86_REG_EBX,0x98765432),(UC_X86_REG_ECX,0xabcd12),
                          (UC_X86_REG_EDX,0xabcd34),(UC_X86_REG_EFLAGS,0x246),
                          (UC_X86_REG_XMM1,sentinel1),(UC_X86_REG_XMM2,sentinel2),
                          (UC_X86_REG_XMM5,struct.unpack('<I',f(target))[0])]:uc.reg_write(reg,value)
        uc.emu_start(SITE,SITE+14,count=500)
        target_after=math.atan2(readf(uc,actor+0x1c8),readf(uc,actor+0x1c0))%(2*math.pi)
        assert abs(angle_delta(readf(uc,obj+0x11c),target_after))<2e-6
        assert uc.reg_read(UC_X86_REG_ESP)==esp
        assert uc.reg_read(UC_X86_REG_XMM1)==sentinel1
        assert uc.reg_read(UC_X86_REG_XMM2)==sentinel2
        assert uc.mem_read(actor+0x5e0,16)==uc.mem_read(actor+0x1c0,16)

for rate in [1.5,2.25,4.5]:
    for x in [-1,-0.3,0.3,1]:
        for fps in [30,60,120]:run(rate,x,fps,0.2)

for name in ['Precision','Navigation','Inventory']:
    for stacked in [False,True]:
        uc=Uc(UC_ARCH_X86,UC_MODE_32)
        for a,n in [(0x10385000,0x2000),(0x11589000,0x1000),(0x200000,0x7000),(0x400000,0x2000)]:uc.mem_map(a,n)
        uc.mem_write(AIM_SITE,image[offset(AIM_SITE,8):offset(AIM_SITE,8)+8]);uc.mem_write(AIM_CAVE,aim)
        uc.mem_write(AIM_X,f(2));uc.mem_write(AIM_Y,f(3))
        uc.mem_write(AIM_INPUT_REFERENCE,f(2));uc.mem_write(AIM_FLAG,u(0x206800))
        uc.mem_write(0x206800,u(0))
        world,manager,camera,string,array,actor=0x200000,0x201000,0x202000,0x203000,0x204000,0x205000
        uc.mem_write(0x1158982c,u(world));uc.mem_write(world+8,u(manager))
        uc.mem_write(manager+0x288,u(1 if stacked else 0));uc.mem_write(manager+0x28c,u(array))
        uc.mem_write(manager+0x2b0,u(camera));uc.mem_write(array+4,u(camera))
        uc.mem_write(camera+0x248,u(string));uc.mem_write(string,name.encode()+b'\0')
        uc.mem_write(actor+0xae8,f(0.4));uc.mem_write(actor+0xaec,f(-0.2));uc.mem_write(actor+0xad8,f(0.1))
        uc.reg_write(UC_X86_REG_ESP,0x401000);uc.reg_write(UC_X86_REG_ESI,actor)
        sentinel=0x1234567890abcdef0011223344556677;uc.reg_write(UC_X86_REG_XMM0,sentinel)
        uc.emu_start(AIM_SITE,AIM_SITE+8,count=300)
        assert math.isclose(readf(uc,actor+0xae8),0.8 if name=='Precision' else 0.4,abs_tol=1e-6)
        assert math.isclose(readf(uc,actor+0xaec),-0.4 if name=='Precision' else -0.2,abs_tol=1e-6)
        assert readu(uc,0x206800)==(1 if name=='Precision' else 0)
        assert uc.reg_read(UC_X86_REG_XMM0)==sentinel and uc.reg_read(UC_X86_REG_ESP)==0x401000
print('PASS: 10800 sustained heading frames at 30/60/120 FPS; Precision-only gain in stacked/default cameras. Engine internals and visual result require gameplay.')
