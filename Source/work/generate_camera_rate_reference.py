"""Derive vertical full-deflection parity from the original native constants."""
from pathlib import Path
import struct,hashlib,json,sys
sys.path.insert(0,str(Path(__file__).parent/'pydeps'))
from build_navigation_bounded_yaw import offset
P=Path(__file__).resolve().parent.parent
M=Path((P/'work/camera_package_path.txt').read_text(encoding='utf-8').strip())
source=(M/'Backup Original/Bin/g_SilentHill.sgl').read_bytes()
assert hashlib.sha256(source).hexdigest().upper()=='2A7C30031A3146036115292EED7D6022C603470C257A5659BED8D4423F2DFD61'
assert source[offset(0x108DAFFB,8):offset(0x108DAFFB,8)+8]==bytes.fromhex('F2 0F 59 0D 90 12 F9 10')
assert source[offset(0x108DB3A8,6):offset(0x108DB3A8,6)+6]==bytes.fromhex('DC 0D 48 3F F9 10')
pitch_degrees=struct.unpack('<d',source[offset(0x10F91290,8):offset(0x10F91290,8)+8])[0]
degrees_to_radians=struct.unpack('<d',source[offset(0x10F93F48,8):offset(0x10F93F48,8)+8])[0]
horizontal_radians=1.5 # user-approved normal X reference from revision 1.2
native_vertical_radians=pitch_degrees*degrees_to_radians
gain=horizontal_radians/native_vertical_radians
user_vertical_calibration=2.0 # user selected old Y=2.0 as the new Y=1.0
(P/'navigation_rate_reference.h').write_text(f'''// Derived from original SGL; full controller deflection, before pitch clamps.
#define CAMERA_HORIZONTAL_REFERENCE {horizontal_radians:.17g}f
#define CAMERA_NATIVE_VERTICAL_DEGREES {pitch_degrees:.17g}
#define CAMERA_DEGREES_TO_RADIANS {degrees_to_radians:.17g}
#define CAMERA_VERTICAL_REFERENCE_GAIN {gain:.17g}
#define CAMERA_VERTICAL_USER_CALIBRATION {user_vertical_calibration:.17g}
''',encoding='ascii')
(P/'work/camera_rate_reference.json').write_text(json.dumps({'horizontal_radians_per_second':horizontal_radians,'native_vertical_degrees_per_second':pitch_degrees,'native_degrees_to_radians':degrees_to_radians,'vertical_gain':gain,'user_vertical_calibration':user_vertical_calibration,'effective_vertical_gain':gain*user_vertical_calibration,'native_vertical_curve':'quadratic','mod_vertical_curve':'linear','basis':'User feedback: new Y1.0 equals previous Y2.0; not measured visual parity.'},indent=2)+'\n',encoding='utf-8')
print(f'Full-deflection vertical parity gain={gain:.12f}; native pitch={pitch_degrees:g} deg/s')
