
import os
import sys
import ctypes

print('Current working directory', sys.argv[0])

def get_windows_scaling_factor():
    try:
        # Call the Windows API function to get the scaling factor
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()

        # Calculate the scaling factor
        print("Scaling (SiliconUI)", scaling_factor / 96.0)
        return scaling_factor / 96.0

    except Exception as e:
        print("Unable to get the scaling factor, set to 1, error:", e)
        return 1

SA_SCALE_FACTOR = get_windows_scaling_factor()
os.environ['QT_SCALE_FACTOR'] = str(SA_SCALE_FACTOR)

from .SiFont import *
from .SiButton import *
from .SiOption import *
from .SiScrollFrame import *
from .SiScrollArea import *
from .SiTab import *
from .SiTabArea import *
from .SiInfo import *
from .SiLabel import *
from .SiTable import *
from .SiProgressBar import *
from .SiSticker import *
