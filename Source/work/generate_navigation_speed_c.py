from pathlib import Path
from build_navigation_response import build,AIM_SITE,AIM_CAVE,AIM_OUTPUT_X_SITE,AIM_OUTPUT_Y_SITE,AIM_OUTPUT_X_CAVE,AIM_OUTPUT_Y_CAVE,PITCH_MASK,AIM_INPUT_REFERENCE
from build_navigation_actor_yaw import SITE,CAVE,HELPER,offset
from build_navigation_xy import SITE_A,SITE_B
image,code,helper,aim=build()
xy=image
def array(name,data):return 'static const unsigned char '+name+'[]={'+','.join('0x%02x'%b for b in data)+'};\n'
p=Path(__file__).resolve().parent.parent/'navigation_speed_signatures.h'
p.write_text(array('expected_hook',image[offset(SITE,6):offset(SITE,6)+6])+
             array('expected_code',code)+array('expected_helper',helper)+
             array('expected_pitch_a',xy[offset(SITE_A,8):offset(SITE_A,8)+8])+
             array('expected_pitch_b',xy[offset(SITE_B,8):offset(SITE_B,8)+8])+
             array('expected_pitch_code_a',xy[offset(CAVE+0x200,0x40):offset(CAVE+0x200,0x40)+0x40])+
             array('expected_pitch_code_b',xy[offset(CAVE+0x240,0x40):offset(CAVE+0x240,0x40)+0x40])+
             array('expected_aim_hook',image[offset(AIM_SITE,8):offset(AIM_SITE,8)+8])+
             array('expected_aim_code',aim)+
             array('expected_pitch_mask',image[offset(PITCH_MASK,16):offset(PITCH_MASK,16)+16])+
             array('expected_aim_reference',image[offset(AIM_INPUT_REFERENCE,4):offset(AIM_INPUT_REFERENCE,4)+4])+
             array('expected_aim_x_hook',image[offset(AIM_OUTPUT_X_SITE,8):offset(AIM_OUTPUT_X_SITE,8)+8])+
             array('expected_aim_y_hook',image[offset(AIM_OUTPUT_Y_SITE,6):offset(AIM_OUTPUT_Y_SITE,6)+6])+
             array('expected_aim_x_code',image[offset(AIM_OUTPUT_X_CAVE,0x80):offset(AIM_OUTPUT_X_CAVE,0x80)+0x80])+
             array('expected_aim_y_code',image[offset(AIM_OUTPUT_Y_CAVE,0x80):offset(AIM_OUTPUT_Y_CAVE,0x80)+0x80]),encoding='ascii')
