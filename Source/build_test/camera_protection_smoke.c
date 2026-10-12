// Execute the real x86 input detour with executable pages READ/EXECUTE only.
#include "../src/camera_speed_wrapper.c"
static void run_input(void *entry,void *actor){
    __asm__ volatile("call *%1" : "+S"(actor) : "r"(entry)
                     : "eax","ecx","edx","xmm0","xmm1","memory","cc");
}
static void put_u(unsigned char *p,DWORD value){copy(p,(unsigned char*)&value,4);}
static void put_f(unsigned char *p,float value){copy(p,(unsigned char*)&value,4);}
static int test(void){
    unsigned char *image=VirtualAlloc((void*)0x10000000,0x1a00000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);
    IMAGE_DOS_HEADER *dos;IMAGE_NT_HEADERS32 *nt;DWORD old,ignored,address;
    unsigned char *world,*manager,*camera,*name,*actor;
    const unsigned char precision[]="Precision",navigation[]="Navigation";
    if(image!=(unsigned char*)0x10000000)return 1;
    dos=(void*)image;dos->e_magic=IMAGE_DOS_SIGNATURE;dos->e_lfanew=0x80;
    nt=(void*)(image+0x80);nt->Signature=IMAGE_NT_SIGNATURE;nt->FileHeader.Machine=IMAGE_FILE_MACHINE_I386;
    nt->OptionalHeader.Magic=IMAGE_NT_OPTIONAL_HDR32_MAGIC;nt->OptionalHeader.SizeOfImage=0x1a00000;
    copy(image+0x8db3d6,expected_hook,sizeof(expected_hook));copy(image+0x386000,expected_code,sizeof(expected_code));
    copy(image+0x386100,expected_helper,sizeof(expected_helper));copy(image+0x8daffb,expected_pitch_a,sizeof(expected_pitch_a));
    copy(image+0x8db012,expected_pitch_b,sizeof(expected_pitch_b));copy(image+0x386200,expected_pitch_code_a,sizeof(expected_pitch_code_a));
    copy(image+0x386240,expected_pitch_code_b,sizeof(expected_pitch_code_b));copy(image+0x3851e0,expected_aim_hook,sizeof(expected_aim_hook));
    copy(image+0x386300,expected_aim_code,sizeof(expected_aim_code));copy(image+0x3862d0,expected_pitch_mask,sizeof(expected_pitch_mask));
    copy(image+0x3863fc,expected_aim_reference,sizeof(expected_aim_reference));copy(image+0x711f24,expected_aim_x_hook,sizeof(expected_aim_x_hook));
    copy(image+0x71ea28,expected_aim_y_hook,sizeof(expected_aim_y_hook));copy(image+0x386400,expected_aim_x_code,sizeof(expected_aim_x_code));
    copy(image+0x386480,expected_aim_y_code,sizeof(expected_aim_y_code));
    image[0x3851e8]=0xc3; // Controlled continuation: native MOVSS then return.
    if(!VirtualProtect(image+0x385000,0x2000,PAGE_EXECUTE_READ,&old))return 2;
    if(apply_image(image,1,1,1,1)!=1)return 3;
    copy((unsigned char*)&address,image+0x3863f8,4);
    if(address!=(DWORD)(ULONG_PTR)&precision_mode)return 4;
    actor=image+0x1604000;put_f(actor+0xad8,0.1f);
    precision_mode=9;
    run_input(image+0x3851e0,actor); // World pointer is null: reset in writable data.
    if(precision_mode!=0)return 5;
    world=image+0x1600000;manager=image+0x1601000;camera=image+0x1602000;name=image+0x1603000;
    put_u(image+0x158982c,(DWORD)(ULONG_PTR)world);put_u(world+8,(DWORD)(ULONG_PTR)manager);
    put_u(manager+0x288,0);put_u(manager+0x2b0,(DWORD)(ULONG_PTR)camera);put_u(camera+0x248,(DWORD)(ULONG_PTR)name);
    copy(name,precision,sizeof(precision));put_f(actor+0xae8,0.25f);put_f(actor+0xaec,-0.5f);
    run_input(image+0x3851e0,actor);
    if(precision_mode!=1||*(float*)(actor+0xae8)!=0.5f||*(float*)(actor+0xaec)!=-1.0f)return 6;
    copy(name,navigation,sizeof(navigation));put_f(actor+0xae8,0.25f);put_f(actor+0xaec,-0.5f);
    run_input(image+0x3851e0,actor);
    if(precision_mode!=0||*(float*)(actor+0xae8)!=0.25f||*(float*)(actor+0xaec)!=-0.5f)return 7;
    // Unconfigured SGL must not dereference a null state pointer.
    if(!VirtualProtect(image+0x3863f8,4,PAGE_EXECUTE_READWRITE,&old))return 8;
    put_u(image+0x3863f8,0);
    if(!VirtualProtect(image+0x3863f8,4,old,&ignored))return 9;
    run_input(image+0x3851e0,actor);
    VirtualFree(image,0,MEM_RELEASE);
    return 0;
}
void WINAPI start(void){ExitProcess(test());}
