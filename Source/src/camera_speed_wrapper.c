// Lightweight x86 wrapper: preserve the existing input DLL, configure the
// gameplay-confirmed SGL rate, and forward XInput without changing its data.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <Xinput.h>
#include "navigation_speed_signatures.h"
#include "navigation_rate_reference.h"
static HMODULE self_module, base_module;
static volatile LONG initialized, configured;
static DWORD (WINAPI *base_state)(DWORD,XINPUT_STATE*);
static DWORD (WINAPI *base_set)(DWORD,XINPUT_VIBRATION*);
static DWORD (WINAPI *base_caps)(DWORD,DWORD,XINPUT_CAPABILITIES*);
static float speed_x=1.0f,speed_y=1.0f;
static float aim_x=1.0f,aim_y=1.0f;
// Runtime state belongs to writable DLL data, never to executable SGL pages.
static DWORD precision_mode;

static unsigned int length(const char *s){unsigned int n=0;while(s[n])++n;return n;}
static int equal(const unsigned char *a,const unsigned char *b,unsigned int n){while(n--)if(*a++!=*b++)return 0;return 1;}
static void copy(unsigned char *a,const unsigned char *b,unsigned int n){while(n--)*a++=*b++;}
static int sibling(char *out,const char *name){
    DWORD n=GetModuleFileNameA(self_module,out,MAX_PATH);unsigned int i,j;
    if(!n||n>=MAX_PATH)return 0;
    for(i=n;i>0;--i)if(out[i-1]=='\\'||out[i-1]=='/')break;
    if(i+length(name)>=MAX_PATH)return 0;
    for(j=0;name[j];++j)out[i+j]=name[j];out[i+j]=0;return 1;
}
static float parse_speed(const char *p){
    unsigned int digits=0;float value=0,place=0.1f;
    while(*p==' '||*p=='\t')++p;
    while(*p>='0'&&*p<='9'){value=value*10+(*p++-'0');++digits;if(value>100)return 1.0f;}
    if(*p=='.'){++p;while(*p>='0'&&*p<='9'){value+=(*p++-'0')*place;place*=0.1f;++digits;}}
    while(*p==' '||*p=='\t')++p;
    if(!digits||*p)return 1.0f;
    return value<0.25f?0.25f:value>3.0f?3.0f:value;
}
static void log_speed(const char *message){
    char path[MAX_PATH];HANDLE file;DWORD written;
    if(!sibling(path,"camera_axis_fix.log"))return;
    file=CreateFileA(path,FILE_APPEND_DATA,FILE_SHARE_READ|FILE_SHARE_WRITE,0,OPEN_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);
    if(file==INVALID_HANDLE_VALUE)return;
    WriteFile(file,message,length(message),&written,0);CloseHandle(file);
}
// No disk modification: Navigation horizontal rate and two vertical branches.
static int apply_image(unsigned char *base,float horizontal,float vertical,float aim_horizontal,float aim_vertical){
    IMAGE_DOS_HEADER *dos=(IMAGE_DOS_HEADER*)base;IMAGE_NT_HEADERS32 *nt;
    unsigned char *code,*pitch;DWORD previous,previous_pitch,ignored;
    float rate=CAMERA_HORIZONTAL_REFERENCE*horizontal;
    float vertical_float=(float)(CAMERA_VERTICAL_REFERENCE_GAIN*CAMERA_VERTICAL_USER_CALIBRATION*(double)vertical);
    float aim_gains[2]={aim_horizontal/3.0f,aim_vertical/3.0f};
    double vertical_double=CAMERA_VERTICAL_REFERENCE_GAIN*CAMERA_VERTICAL_USER_CALIBRATION*(double)vertical;
    DWORD mode_address=(DWORD)(ULONG_PTR)&precision_mode;
    if(!base||horizontal<0.25f||horizontal>3.0f||horizontal!=horizontal||
       vertical<0.25f||vertical>3.0f||vertical!=vertical||
       aim_horizontal<0.25f||aim_horizontal>3.0f||aim_horizontal!=aim_horizontal||
       aim_vertical<0.25f||aim_vertical>3.0f||aim_vertical!=aim_vertical)return -1;
    if(dos->e_magic!=IMAGE_DOS_SIGNATURE||dos->e_lfanew<0x40||dos->e_lfanew>0x1000)return -1;
    nt=(IMAGE_NT_HEADERS32*)(base+dos->e_lfanew);
    if(nt->Signature!=IMAGE_NT_SIGNATURE||nt->FileHeader.Machine!=IMAGE_FILE_MACHINE_I386||
       nt->OptionalHeader.Magic!=IMAGE_NT_OPTIONAL_HDR32_MAGIC||nt->OptionalHeader.SizeOfImage<0x8db3dc)return -1;
    code=base+0x386000;
    pitch=base+0x386200;
    if(!equal(base+0x8db3d6,expected_hook,sizeof(expected_hook))||
       !equal(code,expected_code,15)||!equal(code+19,expected_code+19,sizeof(expected_code)-19)||
       !equal(base+0x386100,expected_helper,sizeof(expected_helper))||
       !equal(base+0x8daffb,expected_pitch_a,sizeof(expected_pitch_a))||
       !equal(base+0x8db012,expected_pitch_b,sizeof(expected_pitch_b))||
       !equal(pitch,expected_pitch_code_a,sizeof(expected_pitch_code_a))||
       !equal(pitch+0x40,expected_pitch_code_b,sizeof(expected_pitch_code_b))||
       !equal(base+0x3851e0,expected_aim_hook,sizeof(expected_aim_hook))||
       !equal(base+0x386300,expected_aim_code,sizeof(expected_aim_code))||
       !equal(base+0x3862d0,expected_pitch_mask,sizeof(expected_pitch_mask))||
       !equal(base+0x3863fc,expected_aim_reference,sizeof(expected_aim_reference))||
       !equal(base+0x711f24,expected_aim_x_hook,sizeof(expected_aim_x_hook))||
       !equal(base+0x71ea28,expected_aim_y_hook,sizeof(expected_aim_y_hook))||
       !equal(base+0x386400,expected_aim_x_code,sizeof(expected_aim_x_code))||
       !equal(base+0x386480,expected_aim_y_code,sizeof(expected_aim_y_code)))return -1;
    if(!VirtualProtect(code+15,4,PAGE_EXECUTE_READWRITE,&previous))return -2;
    if(!VirtualProtect(pitch+0xf0,0x10c,PAGE_EXECUTE_READWRITE,&previous_pitch)){
        VirtualProtect(code+15,4,previous,&ignored);return -2;
    }
    copy(code+15,(unsigned char*)&rate,4);
    copy(pitch+0xf0,(unsigned char*)&vertical_double,8);
    copy(pitch+0xf8,(unsigned char*)&vertical_float,4);
    copy(base+0x3863f0,(unsigned char*)aim_gains,8);
    precision_mode=0;
    copy(base+0x3863f8,(unsigned char*)&mode_address,4);
    FlushInstructionCache(GetCurrentProcess(),code+15,4);
    FlushInstructionCache(GetCurrentProcess(),pitch+0xf0,0x10c);
    if(!VirtualProtect(pitch+0xf0,0x10c,previous_pitch,&ignored))return -2;
    if(!VirtualProtect(code+15,4,previous,&ignored))return -2;
    return 1;
}
static int initialize(void){
    char path[MAX_PATH],value[32];LONG status=InterlockedCompareExchange(&initialized,1,0);
    if(status==0){
        if(sibling(path,"camera_axis_fix.ini")){
            GetPrivateProfileStringA("Camera","HorizontalCameraSpeed","1.0",value,sizeof(value),path);
            speed_x=parse_speed(value);
            GetPrivateProfileStringA("Camera","VerticalCameraSpeed","1.0",value,sizeof(value),path);
            speed_y=parse_speed(value);
            GetPrivateProfileStringA("Camera","AimHorizontalSpeed","1.0",value,sizeof(value),path);
            aim_x=parse_speed(value);
            GetPrivateProfileStringA("Camera","AimVerticalSpeed","1.0",value,sizeof(value),path);
            aim_y=parse_speed(value);
        }
        if(sibling(path,"camera_input_base.dll"))base_module=LoadLibraryA(path);
        if(base_module){
            base_state=(void*)GetProcAddress(base_module,"XInputGetState");
            base_set=(void*)GetProcAddress(base_module,"XInputSetState");
            base_caps=(void*)GetProcAddress(base_module,"XInputGetCapabilities");
        }
        InterlockedExchange(&initialized,2);
    }else while(InterlockedCompareExchange(&initialized,2,2)!=2)Sleep(0);
    return base_state&&base_set&&base_caps;
}
BOOL WINAPI DllMain(HINSTANCE module,DWORD reason,LPVOID reserved){
    if(reason==DLL_PROCESS_ATTACH){self_module=module;DisableThreadLibraryCalls(module);}return TRUE;
}
DWORD WINAPI ProxyXInputGetState(DWORD user,XINPUT_STATE *state){
    HMODULE engine;
    if(!initialize())return ERROR_DEVICE_NOT_CONNECTED;
    engine=GetModuleHandleA("g_SilentHill.sgl");
    if(engine&&InterlockedCompareExchange(&configured,1,0)==0){
        int result=apply_image((unsigned char*)engine,speed_x,speed_y,aim_x,aim_y);
        if(result==1){
            char message[]="Navigation speed: X=0.00 Y=0.00; applied.\r\n";
            char *value=message+sizeof("Navigation speed: X=")-1;
            unsigned int scaled=(unsigned int)(speed_x*100.0f+0.5f);
            value[0]='0'+scaled/100;value[2]='0'+scaled/10%10;value[3]='0'+scaled%10;
            value+=7;scaled=(unsigned int)(speed_y*100.0f+0.5f);
            value[0]='0'+scaled/100;value[2]='0'+scaled/10%10;value[3]='0'+scaled%10;
            log_speed(message);
            char aim_message[]="Precision speed: X=0.00 Y=0.00; post-curve scale=value/3; applied.\r\n";
            value=aim_message+sizeof("Precision speed: X=")-1;
            scaled=(unsigned int)(aim_x*100.0f+0.5f);
            value[0]='0'+scaled/100;value[2]='0'+scaled/10%10;value[3]='0'+scaled%10;
            value+=7;scaled=(unsigned int)(aim_y*100.0f+0.5f);
            value[0]='0'+scaled/100;value[2]='0'+scaled/10%10;value[3]='0'+scaled%10;
            log_speed(aim_message);
        }
        else log_speed("Navigation speed: rejected; unsupported SGL or memory protection failure.\r\n");
    }
    return base_state(user,state);
}
DWORD WINAPI ProxyXInputSetState(DWORD user,XINPUT_VIBRATION *vibration){
    return initialize()?base_set(user,vibration):ERROR_DEVICE_NOT_CONNECTED;
}
DWORD WINAPI ProxyXInputGetCapabilities(DWORD user,DWORD flags,XINPUT_CAPABILITIES *caps){
    return initialize()?base_caps(user,flags,caps):ERROR_DEVICE_NOT_CONNECTED;
}
