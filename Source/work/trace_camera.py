import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pydeps'))
import capstone
import pefile

PATH = r'F:\Jogos\Silent Hill (TUDO)\Silent Hill 5 - Homecoming\Silent Hill 5 - Homecoming (Update 3.20)(PT-BR) - [PC]-By Emerson Teles\Bin\g_SilentHill.sgl'
data = open(PATH, 'rb').read()
pe = pefile.PE(data=data, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
sections = [(s.Name.rstrip(b'\0').decode(), base+s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
def chunk(va, size):
    for _, start, offset, length in sections:
        if start <= va and va+size <= start+length:
            return data[offset+va-start:offset+va-start+size]
    raise ValueError(hex(va))
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
cs.detail = True
cs.skipdata = True
def dis(start, end):
    for ins in cs.disasm(chunk(start,end-start),start):
        print(f'{ins.address:08X} {ins.mnemonic:8s} {ins.op_str}')

if __name__ == '__main__':
    print('sections', sections)
    for a,b in [(0x102c73e0,0x102c75b7),(0x1003ac90,0x1003acc0),(0x10384e80,0x10385030)]:
        print(f'\n--- {a:08X} ---')
        dis(a,b)
    targets={0x102c73e0,0x1003acab}
    for name,va,off,length in sections:
        if name != '.text': continue
        print(f'\nDirect references to {targets}:')
        for ins in cs.disasm(data[off:off+length],va):
            if ins.id == 0: continue
            for op in ins.operands:
                if op.type == capstone.x86.X86_OP_IMM and op.imm in targets:
                    print(f'{ins.address:08X} {ins.mnemonic} {ins.op_str}')
