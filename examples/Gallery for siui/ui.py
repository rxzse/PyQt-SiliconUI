import icons
from components.page_about import About
from components.page_dialog import ExampleDialogs
from components.page_homepage import ExampleHomepage
from components.page_icons import ExampleIcons
from components.page_option_cards import ExampleOptionCards
from components.page_widgets import ExampleWidgets
from components.page_container import ExampleContainer
from components.page_functional import ExampleFunctional
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget

import siui
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.templates.application.application import SiliconApplication

# 载入图标
siui.core.globals.SiGlobal.siui.loadIcons(
    icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
)


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.setMinimumSize(1024, 380)
        self.resize(1366, 916)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Silicon UI Gallery")
        self.setWindowTitle("Silicon UI Gallery")
        self.setWindowIcon(QIcon("./img/empty_icon.png"))

        self.layerMain().addPage(ExampleHomepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="Homepage", side="top")
        self.layerMain().addPage(ExampleIcons(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_diversity_filled"),
                                 hint="Icon Packs", side="top")
        self.layerMain().addPage(ExampleWidgets(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_box_multiple_filled"),
                                 hint="Controls", side="top")
        self.layerMain().addPage(ExampleContainer(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_align_stretch_vertical_filled"),
                                 hint="Container", side="top")
        self.layerMain().addPage(ExampleOptionCards(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_list_bar_filled"),
                                 hint="Tabs", side="top")
        self.layerMain().addPage(ExampleDialogs(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_panel_separate_window_filled"),
                                 hint="Messages/Dialogs", side="top")
        self.layerMain().addPage(ExampleFunctional(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_puzzle_piece_filled"),
                                 hint="Functional Components", side="top")

        self.layerMain().addPage(About(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="About me", side="bottom")

        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()
