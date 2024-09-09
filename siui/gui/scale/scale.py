import ctypes
import os


def get_windows_scaling_factor():
    try:
        # Call the Windows API function to get the scaling factor
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()

        # Calculate the scaling factor
        return scaling_factor / 96.0

    except Exception as e:
        print("Unable to get the zoom ratio, set to 1, error:", e)
        return 1


def reload_scale_factor():
    set_scale_factor(get_windows_scaling_factor(), identity="Windows API")


def set_scale_factor(factor, identity="External calls"):
    os.environ["QT_SCALE_FACTOR"] = str(factor)
    print("The environment variable QT_SCALE_FACTOR has been set to", factor, f" (Source: {identity})")
