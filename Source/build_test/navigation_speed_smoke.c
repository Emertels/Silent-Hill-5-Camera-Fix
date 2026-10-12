#include "../src/camera_speed_wrapper.c"
static int values_close(float a,float b){return a-b<0.000001f && b-a<0.000001f;}
static int tests(void){
    unsigned char *image=VirtualAlloc(0,0xa00000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);
    IMAGE_DOS_HEADER *dos;IMAGE_NT_HEADERS32 *nt;unsigned int i;
    float values[]={0.25f,0.5f,0.75f,1.0f,1.5f,2.0f,3.0f};float actual,actual_y;
    double actual_y_double;
    if(!image)return 1;
    dos=(IMAGE_DOS_HEADER*)image;dos->e_magic=IMAGE_DOS_SIGNATURE;dos->e_lfanew=0x80;
    nt=(IMAGE_NT_HEADERS32*)(image+0x80);nt->Signature=IMAGE_NT_SIGNATURE;
    nt->FileHeader.Machine=IMAGE_FILE_MACHINE_I386;
    nt->OptionalHeader.Magic=IMAGE_NT_OPTIONAL_HDR32_MAGIC;nt->OptionalHeader.SizeOfImage=0xa00000;
    copy(image+0x8db3d6,expected_hook,sizeof(expected_hook));
    copy(image+0x386000,expected_code,sizeof(expected_code));
    copy(image+0x386100,expected_helper,sizeof(expected_helper));
    copy(image+0x8daffb,expected_pitch_a,sizeof(expected_pitch_a));
    copy(image+0x8db012,expected_pitch_b,sizeof(expected_pitch_b));
    copy(image+0x386200,expected_pitch_code_a,sizeof(expected_pitch_code_a));
    copy(image+0x386240,expected_pitch_code_b,sizeof(expected_pitch_code_b));
    copy(image+0x3851e0,expected_aim_hook,sizeof(expected_aim_hook));
    copy(image+0x386300,expected_aim_code,sizeof(expected_aim_code));
    copy(image+0x3862d0,expected_pitch_mask,sizeof(expected_pitch_mask));
    copy(image+0x3863fc,expected_aim_reference,sizeof(expected_aim_reference));
    copy(image+0x711f24,expected_aim_x_hook,sizeof(expected_aim_x_hook));
    copy(image+0x71ea28,expected_aim_y_hook,sizeof(expected_aim_y_hook));
    copy(image+0x386400,expected_aim_x_code,sizeof(expected_aim_x_code));
    copy(image+0x386480,expected_aim_y_code,sizeof(expected_aim_y_code));
    for(i=0;i<sizeof(values)/sizeof(values[0]);++i){
        if(apply_image(image,values[i],values[i],values[i],values[i])!=1)return 2;
        copy((unsigned char*)&actual,image+0x38600f,4);
        copy((unsigned char*)&actual_y_double,image+0x3862f0,8);
        copy((unsigned char*)&actual_y,image+0x3862f8,4);
        if(actual-1.5f*values[i]>0.000001f || 1.5f*values[i]-actual>0.000001f||
           actual_y!=(float)(CAMERA_VERTICAL_REFERENCE_GAIN*CAMERA_VERTICAL_USER_CALIBRATION*(double)values[i])||
           actual_y_double!=CAMERA_VERTICAL_REFERENCE_GAIN*CAMERA_VERTICAL_USER_CALIBRATION*(double)values[i])return 3;
        // User chose old Y=2 as new Y=1; test that explicit normalization.
        double pitch_rate=CAMERA_NATIVE_VERTICAL_DEGREES*CAMERA_DEGREES_TO_RADIANS*actual_y_double;
        double calibrated_reference=(double)actual*CAMERA_VERTICAL_USER_CALIBRATION;
        if(pitch_rate-calibrated_reference>0.000001 || calibrated_reference-pitch_rate>0.000001)return 12;
        copy((unsigned char*)&actual_y,image+0x3863f0,4);
        if(!values_close(actual_y,values[i]/3.0f))return 13;
        copy((unsigned char*)&actual_y,image+0x3863f4,4);
        if(!values_close(actual_y,values[i]/3.0f))return 14;
        if(!equal(image+0x386000,expected_code,15)||
           !equal(image+0x386013,expected_code+19,sizeof(expected_code)-19)||
           !equal(image+0x386100,expected_helper,sizeof(expected_helper)))return 4;
    }
    if(apply_image(image,1.0f,1.0f,1.0f,1.0f)!=1)return 5;
    image[0x386110]^=1;
    if(apply_image(image,2.0f,2.0f,1.0f,1.0f)!=-1)return 6;
    copy((unsigned char*)&actual,image+0x38600f,4);if(actual!=1.5f)return 7;
    if(!values_close(parse_speed("0.5"),0.5f)||!values_close(parse_speed("1.5"),1.5f)||!values_close(parse_speed("2.0"),2.0f)||
       parse_speed("1,5")!=1.0f||parse_speed("junk")!=1.0f||
       parse_speed("0")!=0.25f||parse_speed("4")!=3.0f)return 8;
    VirtualFree(image,0,MEM_RELEASE);
    {
        HMODULE wrapper=LoadLibraryA("build_test\\xinput1_3_configurable.dll");
        HMODULE preserved=LoadLibraryA("build_test\\camera_input_base.dll");
        DWORD (WINAPI *get)(DWORD,XINPUT_STATE*), (WINAPI *old_get)(DWORD,XINPUT_STATE*);
        XINPUT_STATE one={0},two={0};DWORD a,b;
        if(!wrapper||!preserved)return 9;
        get=(void*)GetProcAddress(wrapper,"XInputGetState");
        old_get=(void*)GetProcAddress(preserved,"XInputGetState");
        if(!get||!old_get||!GetProcAddress(wrapper,"XInputSetState")||
           !GetProcAddress(wrapper,"XInputGetCapabilities"))return 10;
        a=get(7,&one);b=old_get(7,&two);if(a!=b)return 11;
    }
    return 0;
}
void WINAPI start(void){ExitProcess(tests());}
