from PyQt5.QtCore import Qt

from siui.components.widgets.container import SiDenseHContainer, SiDenseVContainer
from siui.components.widgets.label import SiLabel
from siui.components.widgets.scrollarea import SiScrollArea
from siui.core.globals import SiGlobal
from siui.core.silicon import Si


class SiPage(SiDenseVContainer):
    """ Page class, which is instantiated as a single page in SiliconApplication """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSpacing(0)
        self.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        self.scroll_maximum_width = 10000   # 滚动区域宽度限制
        self.title_height = 0               # 标题引入的高度偏移，内容的高度要减去标题的高度
        self.padding = 0                    # 左右空白区域的宽度

        # 滚动区域对齐方式
        self.scroll_alignment = Qt.AlignCenter

        # 滚动区域
        self.scroll_area = SiScrollArea(self)
        self.setAdjustWidgetsSize(True)

        # 添加到垂直容器
        self.addWidget(self.scroll_area)

    def setAttachment(self, widget):
        """ Setting up child controls """
        self.scroll_area.setAttachment(widget)

    def attachment(self):
        """ Get child controls """
        return self.scroll_area.attachment()

    def setScrollMaximumWidth(self, width: int):
        """
        Sets the maximum width of the scroll area's child controls
        :param width: Maximum Width
        """
        self.scroll_maximum_width = width
        self.resize(self.size())

    def setScrollAlignment(self, a0):
        """
        Set the scroll area alignment
        :param a0: Qt enumeration values
        """
        self.scroll_alignment = a0
        self.resize(self.size())

    def setPadding(self, padding):
        """
        The distance between the content and the border
        :param padding: Number of pixels
        """
        self.padding = padding
        self.resize(self.size())

    def setTitle(self, title: str):
        """
        Set the page title
        :param title: title
        """
        # 套标题用的水平容器
        self.title_container = SiDenseHContainer(self)
        self.title_container.setSpacing(0)
        self.title_container.setFixedHeight(32)
        self.title_container.setAlignment(Qt.AlignCenter)

        # 标题
        self.title = SiLabel(self)
        self.title.setFont(SiGlobal.siui.fonts["L_BOLD"])
        self.title.setFixedHeight(32)
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)

        # 添加到水平容器
        self.title_container.addPlaceholder(64)
        self.title_container.addWidget(self.title)

        self.title.setText(title)

        # 添加到垂直容器
        self.addPlaceholder(32, index=0)
        self.addWidget(self.title_container, index=0)
        self.addPlaceholder(32, index=0)

        self.title_height = 96

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()

        self.scroll_area.resize(size.width(), size.height() - self.title_height)
        self.scroll_area.attachment().setFixedWidth(min(size.width() - self.padding * 2, self.scroll_maximum_width))

        # 处理对齐
        if (self.scroll_alignment & Qt.AlignHCenter) == Qt.AlignHCenter:
            scroll_widget_x = (size.width() - self.scroll_area.attachment().width())//2
        elif (self.scroll_alignment & Qt.AlignLeft) == Qt.AlignLeft:
            scroll_widget_x = self.padding
        elif (self.scroll_alignment & Qt.AlignRight) == Qt.AlignRight:
            scroll_widget_x = size.width() - self.scroll_area.attachment().width() - self.padding
        else:
            raise ValueError(f"Invalid alignment value: {self.scroll_alignment}")

        scroll_widget_y = self.scroll_area.attachment().y()

        self.scroll_area.attachment().move(scroll_widget_x, scroll_widget_y)
        self.scroll_area.animationGroup().fromToken("scroll").setTarget([scroll_widget_x, scroll_widget_y])
        self.scroll_area.animationGroup().fromToken("scroll").setCurrent([scroll_widget_x, scroll_widget_y])
