"""Test partial-stick angular parity and Precision post-curve proportionality."""
import sys,struct,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'pydeps'))
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import *
from build_navigation_response import build,offset,CAVE,PITCH_MASK,AIM_X,AIM_Y,AIM_FLAG,AIM_OUTPUT_X_SITE,AIM_OUTPUT_Y_SITE,AIM_OUTPUT_X_CAVE,AIM_OUTPUT_Y_CAVE
image,code,helper,aim=build()
reference=json.loads((Path(__file__).parent/'camera_rate_reference.json').read_text())
gain=reference.get('effective_vertical_gain',reference['vertical_gain']);rad=reference['native_degrees_to_radians']
calibration=reference.get('user_vertical_calibration',1.0)
def f(x):return struct.pack('<f',x)
def d(x):return struct.pack('<d',x)
def u(x):return struct.pack('<I',x)
def readf(uc,a):return struct.unpack('<f',uc.mem_read(a,4))[0]
cases=0
for input_y in [-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1]:
    for multiplier in [1,1.5,2,2.5,3]:
        for fps in [30,60,120]:
            uc=Uc(UC_ARCH_X86,UC_MODE_32)
            for a,n in [(CAVE,0x1000),(0x108db000,0x1000),(0x10f91000,0x1000),(0x300000,0x1000)]:uc.mem_map(a,n)
            uc.mem_write(CAVE+0x200,image[offset(CAVE+0x200,0x40):offset(CAVE+0x200,0x40)+0x40])
            uc.mem_write(PITCH_MASK,image[offset(PITCH_MASK,16):offset(PITCH_MASK,16)+16])
            uc.mem_write(CAVE+0x2f0,d(gain*multiplier));uc.mem_write(0x10f91290,d(60))
            uc.mem_write(0x108db003,image[offset(0x108db003,8):offset(0x108db003,8)+8])
            uc.mem_write(0x300024,f(input_y));uc.reg_write(UC_X86_REG_EBX,0x300000)
            uc.reg_write(UC_X86_REG_XMM0,int.from_bytes(d(1/fps),'little'))
            uc.reg_write(UC_X86_REG_XMM1,int.from_bytes(d(input_y*input_y),'little'))
            uc.emu_start(CAVE+0x200,0x108db00b,count=30)
            degrees=struct.unpack('<f',(uc.reg_read(UC_X86_REG_XMM0)&0xffffffff).to_bytes(4,'little'))[0]
            expected=1.5*calibration*multiplier*abs(input_y)/fps
            assert math.isclose(degrees*rad,expected,abs_tol=1e-8),(input_y,multiplier,fps,degrees*rad,expected)
            cases+=1

for flag in [0,1]:
    for multiplier in [0.25,1,1.5,2,2.5,3]:
        for value in [-4,-0.5,0,0.5,4]:
            for axis in ['X','Y']:
                uc=Uc(UC_ARCH_X86,UC_MODE_32)
                for a,n in [(CAVE,0x1000),(0x10711000,0x1000),(0x1071e000,0x1000),(0x10f8a000,0x1000),(0x400000,0x2000)]:uc.mem_map(a,n)
                site,cave,size=(AIM_OUTPUT_X_SITE,AIM_OUTPUT_X_CAVE,8) if axis=='X' else (AIM_OUTPUT_Y_SITE,AIM_OUTPUT_Y_CAVE,6)
                uc.mem_write(site,image[offset(site,size):offset(site,size)+size])
                uc.mem_write(cave,image[offset(cave,0x80):offset(cave,0x80)+0x80])
                uc.mem_write(AIM_FLAG,u(0x401100));uc.mem_write(0x401100,u(flag))
                uc.mem_write(AIM_X,f(multiplier/3));uc.mem_write(AIM_Y,f(multiplier/3))
                uc.mem_write(0x10f8a2e4,f(1));uc.reg_write(UC_X86_REG_ESP,0x401000)
                uc.reg_write(UC_X86_REG_EFLAGS,0x246)
                uc.mem_write(0x401020,f(value));uc.reg_write(UC_X86_REG_XMM0,int.from_bytes(f(value),'little'))
                uc.emu_start(site,site+size,count=50)
                result=readf(uc,0x401020 if axis=='X' else 0x40101c)
                expected=value*multiplier/3 if flag else value
                assert math.isclose(result,expected,abs_tol=2e-7),(flag,multiplier,axis,value,result,expected)
                assert uc.reg_read(UC_X86_REG_ESP)==0x401000 and uc.reg_read(UC_X86_REG_EFLAGS)==0x246
                cases+=1
print(f'PASS: {cases} response cases; partial-stick pitch parity and post-curve aim scaling, flags/stack intact. Native deadzones/limits and gameplay remain to test.')
