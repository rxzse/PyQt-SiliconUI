from PyQt5.QtCore import pyqtSignal, Qt

from siui.core.globals import SiGlobal
from siui.components.widgets import SiLabel, SiToggleButton
from siui.components.widgets.abstracts import ABCSiNavigationBar
from siui.components.widgets import SiDenseHContainer, SiDenseVContainer, SiStackedContainer
from siui.core.color import SiColor


class PageButton(SiToggleButton):
    activated = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set your own style
        self.setBorderRadius(6)
        self.colorGroup().assign(SiColor.BUTTON_OFF, "#00FFFFFF")
        self.colorGroup().assign(SiColor.BUTTON_ON, "#10FFFFFF")

        # Create a highlight indicator bar to indicate selection
        self.active_indicator = SiLabel(self)
        self.active_indicator.setFixedStyleSheet("border-radius: 2px")
        self.active_indicator.resize(4, 20)
        self.active_indicator.setOpacity(0)

        # How to bind click events to toggle states
        self.clicked.connect(self._on_clicked)

        # Set the self index
        self.index_ = -1

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.active_indicator.setStyleSheet(
            f"background-color: {self.colorGroup().fromToken(SiColor.THEME)}"
        )

    def setActive(self, state):
        """
        Set activation state
        :param state: state
        """
        self.setChecked(state)
        self.active_indicator.setOpacityTo(1 if state is True else 0)
        if state is True:
            self.activated.emit()

    def setIndex(self, index: int):
        """
        Setting the index
        """
        self.index_ = index

    def index(self):
        """
        Get own index
        :return: index
        """
        return self.index_

    def on_index_changed(self, index):
        if index == self.index():
            self.setChecked(True)
            self.active_indicator.setOpacityTo(1)

    def _on_clicked(self):
        self.setActive(True)

        # Traverse all similar child controls under the same parent object and set them all to inactive
        for obj in self.parent().children():
            if isinstance(obj, PageButton) and obj != self:
                obj.setActive(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.active_indicator.move(0, (self.height() - self.active_indicator.height()) // 2)


class PageNavigator(ABCSiNavigationBar):
    """
    Page Navigation Bar
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Clear your own style sheet to prevent inheritance
        self.setStyleSheet("")

        # Create a container to place the button
        self.container = SiDenseVContainer(self)
        self.container.setSpacing(8)
        self.container.setAlignment(Qt.AlignCenter)

        # All Buttons
        self.buttons = []

    def addPageButton(self, svg_data, hint, func_when_active, side="top"):
        """
        Add Page Button
        :param svg_data: The svg data of the button
        :param hint: Tooltips
        :param func_when_active: Function called when activated
        :param side: Which side to add
        """
        new_page_button = PageButton(self)
        new_page_button.setIndex(self.maximumIndex())
        new_page_button.setStyleSheet("background-color: #20FF0000")
        new_page_button.resize(40, 40)
        new_page_button.setHint(hint)
        new_page_button.attachment().setSvgSize(20, 20)
        new_page_button.attachment().load(svg_data)
        new_page_button.activated.connect(func_when_active)

        # Bind the index switching signal. When the page is switched, the button will switch to the checked state.
        self.indexChanged.connect(new_page_button.on_index_changed)

        # The new button is added to the container
        self.container.addWidget(new_page_button, side=side)
        self.setMaximumIndex(self.maximumIndex() + 1)

        self.buttons.append(new_page_button)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()

        self.container.resize(size)


class StackedContainerWithShowUpAnimation(SiStackedContainer):
    def setCurrentIndex(self, index: int):
        super().setCurrentIndex(index)

        self.widgets[index].animationGroup().fromToken("move").setFactor(1 / 5)
        self.widgets[index].move(0, 64)
        self.widgets[index].moveTo(0, 0)


class PageView(SiDenseHContainer):
    """
    Page view, including the navigation bar on the left and the page on the right
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        # Clear your own style sheet to prevent inheritance
        self.setStyleSheet("")

        self.setSpacing(0)
        self.setAdjustWidgetsSize(True)

        # Creating a Navigation Bar
        self.page_navigator = PageNavigator(self)
        self.page_navigator.setFixedWidth(16+24+16)

        # Creating stacked containers
        self.stacked_container = StackedContainerWithShowUpAnimation(self)
        self.stacked_container.setObjectName("stacked_container")

        # <- Add to horizontal layout
        self.addWidget(self.page_navigator)
        self.addWidget(self.stacked_container)

    def _get_page_toggle_method(self, index):
        return lambda: self.stacked_container.setCurrentIndex(index)

    def addPage(self, page, icon, hint, side="top"):
        """
        Add Page, which adds a button to the navbar and adds the page to the stack container
        :param page: Page Control
        :param icon: The svg data or path of the button
        :param hint: Tooltips
        :param side: On which side should the button be added?
        """
        self.stacked_container.addWidget(page)
        self.page_navigator.addPageButton(
            icon,
            hint,
            self._get_page_toggle_method(self.stacked_container.widgetsAmount() - 1),
            side
        )

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.stacked_container.setStyleSheet(
            """
            #stacked_container {{
                border-top-left-radius:6px; border-bottom-right-radius: 8px;
                background-color: {}; border:1px solid {};
            }}
            """.format(SiGlobal.siui.colors["INTERFACE_BG_B"], SiGlobal.siui.colors["INTERFACE_BG_C"])
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.page_navigator.resize(56, h - 8)
        self.stacked_container.setGeometry(56, 0, w-56, h)
