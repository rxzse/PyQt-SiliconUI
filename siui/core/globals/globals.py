import time

from siui.core.color import SiColor
from siui.gui.color_group import DarkColorGroup, BrightColorGroup
from siui.gui.font import GlobalFontDict
from siui.gui.icons.parser import SiGlobalIconPack


class SiliconUIGlobal:
    """
    SiliconUI Global Data used internally\n
    If you also need to use global data, you can add your class to a property of SiGlobal
    """
    # Window dictionary, storing window objects
    windows = {}

    # Color dictionary, stores all dynamically set colors
    # The value is RRGGBB or AARRGGBB color number
    colors = DarkColorGroup()

    # Icon dictionary, storing all SVG type icon data
    # The value is bytes of SVG information
    icons = {}
    iconpack = SiGlobalIconPack()
    iconpack.set_default_color(colors.fromToken(SiColor.SVG_NORMAL))

    # Style sheet dictionary, which stores all dynamic style sheets
    # Value is a string
    qss = {}

    # Font dictionary, stores all fonts
    # The value is a QFont type font
    fonts = GlobalFontDict.fonts

    def loadWindows(self, dictionary):
        SiliconUIGlobal.windows.update(dictionary)

    def loadColors(self, dictionary):
        SiliconUIGlobal.colors.update(dictionary)

    def loadIcons(self, dictionary):
        SiliconUIGlobal.icons.update(dictionary)

    def loadQSS(self, dictionary):
        SiliconUIGlobal.qss.update(dictionary)

    def loadFonts(self, dictionary):
        SiliconUIGlobal.fonts.update(dictionary)

    def reloadAllWindowsStyleSheet(self):
        """
        Call the reloadStyleSheet method in each window and recursively reload the style sheets of all controls in all windows
        """
        for window in self.windows.values():
            try:
                window.reloadStyleSheet()
            except:
                pass
            self._reloadWidgetStyleSheet(window)

    def reloadStyleSheetRecursively(self, widget):
        """ run reloadStyleSheet() for all children of this widget """
        try:
            widget.reloadStyleSheet()
        except:
            pass
        self._reloadWidgetStyleSheet(widget)

    def _reloadWidgetStyleSheet(self, widget):
        for child in widget.children():
            self._reloadWidgetStyleSheet(child)
            try:
                child.reloadStyleSheet()
            except:
                pass
        return


class SiGlobal:
    """
    Global Data\n
    Initialize the variables under .siui when the siui module is imported for the first time
    """
    siui = SiliconUIGlobal()


class NewGlobal:
    """
    New global data
    """
    create_time = time.time()

