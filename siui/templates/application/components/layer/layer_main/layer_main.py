from PyQt5.QtCore import Qt

from siui.components import SiLabel, SiDenseVContainer, SiDenseHContainer, SiPixLabel
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.core.silicon import Si
from siui.templates.application.components.page_view import PageView
from ..layer import SiLayer


class LayerMain(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The bottom label of the entire window
        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")

        # -> A vertical container with a title on top and window content on the bottom
        self.container_title_and_content = SiDenseVContainer(self)
        self.container_title_and_content.setSpacing(0)
        self.container_title_and_content.setAdjustWidgetsSize(True)

        # -> The horizontal container at the title bar has icons and titles on the left and action buttons on the right.
        self.container_title = SiDenseHContainer(self)
        self.container_title.setSpacing(0)
        self.container_title.setAlignment(Qt.AlignCenter)
        self.container_title.setFixedHeight(64)

        # In-app Icon
        self.app_icon = SiPixLabel(self)
        self.app_icon.resize(24, 24)
        self.app_icon.load("./img/logo_new.png")

        # Application Title
        self.app_title = SiLabel(self)
        self.app_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.app_title.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.app_title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.app_title.setText("ZSK Application Template")

        self.container_title.addPlaceholder(2)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_icon)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_title)

        self.page_view = PageView(self)

        # <- Add to vertical container
        self.container_title_and_content.addWidget(self.container_title)
        self.container_title_and_content.addWidget(self.page_view)

        # Hide the shadow layer, as it has no use.
        self.dim_.hide()

    def reloadStyleSheet(self):
        self.background_label.setStyleSheet("background-color: {}; border: 1px solid {};".format(
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_A),
            self.colorGroup().fromToken(SiColor.INTERFACE_BG_B))
        )
        self.app_title.setStyleSheet("color: {}".format(self.colorGroup().fromToken(SiColor.TEXT_B)))

    def setTitle(self, title):
        self.app_title.setText(title)

    def addPage(self, page, icon, hint: str, side="top"):
        """
        Add a New Page
        :param page: Page Control
        :param icon: svg data or path of the page button
        :param hint: Tooltips for page buttons
        :param side: On which side are the page buttons placed?
        """
        self.page_view.addPage(page, icon, hint, side)

    def setPage(self, index):
        """ Set current page by index """
        self.page_view.stacked_container.setCurrentIndex(index)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.resize(event.size())
        self.container_title_and_content.resize(event.size())
        self.page_view.resize(event.size().width(), event.size().height() - 64)
        self.dim_.resize(event.size())
