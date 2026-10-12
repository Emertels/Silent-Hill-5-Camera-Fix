// Patch Fix Camera 1.0 - By Emerson Teles
// Native XInput forwarding with optional right-stick input curves.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <Xinput.h>
static HMODULE module,system_input,crt;
static volatile LONG ready;
static DWORD (WINAPI *state_fn)(DWORD,XINPUT_STATE*);
static DWORD (WINAPI *set_fn)(DWORD,XINPUT_VIBRATION*);
static DWORD (WINAPI *caps_fn)(DWORD,DWORD,XINPUT_CAPABILITIES*);
static float (__cdecl *power_fn)(float,float);
static double (__cdecl *parse_fn)(const char*,char**);
static float exponent_x=1.0f,exponent_y=1.0f,gain_x=1.0f,gain_y=1.0f;
static float clamp(float v,float lo,float hi){return v<lo?lo:(v>hi?hi:v);}
static unsigned int length(const char*s){unsigned int n=0;while(s[n])n++;return n;}
static void append(char*d,const char*s){unsigned int n=length(d),i=0;while(s[i]&&n<MAX_PATH-1)d[n++]=s[i++];d[n]=0;}
static float setting(const char*ini,const char*key,float fallback,float lo,float hi){
    char value[32],*end;double v;
    GetPrivateProfileStringA("Camera",key,"",value,sizeof(value),ini);
    if(!value[0]||!parse_fn)return fallback;
    v=parse_fn(value,&end);
    if(end==value||v!=v||v>3.402823466e38||v< -3.402823466e38)return fallback;
    return clamp((float)v,lo,hi);
}
static SHORT curve(SHORT input,float exponent,float gain){
    int raw=input,magnitude=raw<0?-raw:raw,output;
    float t,curved;
    if(magnitude<=XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE)return 0;
    t=(float)(magnitude-XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE)/(float)(32767-XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE);
    t=clamp(t,0.0f,1.0f);
    curved=exponent==1.0f?t:(power_fn?power_fn(t,exponent):t);
    output=XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE+(int)(curved*gain*(float)(32767-XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE)+0.5f);
    if(output>32767)output=32767;
    return (SHORT)(raw<0?-output:output);
}
static int initialize(void){
    char path[MAX_PATH],ini[MAX_PATH];unsigned int n;
    if(InterlockedCompareExchange(&ready,1,0)==0){
        if(!GetModuleFileNameA(module,ini,MAX_PATH))ini[0]=0;
        n=length(ini);while(n&&ini[n-1]!='\\'&&ini[n-1]!='/')n--;ini[n]=0;
        append(ini,"camera_axis_fix.ini");
        crt=LoadLibraryA("ucrtbase.dll");
        if(crt){power_fn=(void*)GetProcAddress(crt,"powf");parse_fn=(void*)GetProcAddress(crt,"strtod");}
        exponent_x=setting(ini,"RightStickXExponent",1.0f,0.35f,1.0f);
        exponent_y=setting(ini,"RightStickYExponent",1.0f,0.35f,1.0f);
        gain_x=setting(ini,"RightStickXGain",1.0f,0.25f,4.0f);
        gain_y=setting(ini,"RightStickYGain",1.0f,0.25f,4.0f);
        n=GetSystemDirectoryA(path,MAX_PATH);
        if(n&&n<MAX_PATH){append(path,"\\xinput1_3.dll");system_input=LoadLibraryA(path);}
        if(system_input){state_fn=(void*)GetProcAddress(system_input,"XInputGetState");set_fn=(void*)GetProcAddress(system_input,"XInputSetState");caps_fn=(void*)GetProcAddress(system_input,"XInputGetCapabilities");}
        InterlockedExchange(&ready,2);
    }else{while(InterlockedCompareExchange(&ready,2,2)!=2)Sleep(0);}
    return state_fn&&set_fn&&caps_fn;
}
BOOL WINAPI DllMain(HINSTANCE instance,DWORD reason,LPVOID reserved){
    if(reason==DLL_PROCESS_ATTACH){module=instance;DisableThreadLibraryCalls(instance);}return TRUE;
}
DWORD WINAPI ProxyXInputGetState(DWORD user,XINPUT_STATE*state){
    DWORD result;if(!initialize())return ERROR_DEVICE_NOT_CONNECTED;
    result=state_fn(user,state);
    if(result==ERROR_SUCCESS&&state){state->Gamepad.sThumbRX=curve(state->Gamepad.sThumbRX,exponent_x,gain_x);state->Gamepad.sThumbRY=curve(state->Gamepad.sThumbRY,exponent_y,gain_y);}return result;
}
DWORD WINAPI ProxyXInputSetState(DWORD user,XINPUT_VIBRATION*vibration){if(!initialize())return ERROR_DEVICE_NOT_CONNECTED;return set_fn(user,vibration);}
DWORD WINAPI ProxyXInputGetCapabilities(DWORD user,DWORD flags,XINPUT_CAPABILITIES*caps){if(!initialize())return ERROR_DEVICE_NOT_CONNECTED;return caps_fn(user,flags,caps);}
