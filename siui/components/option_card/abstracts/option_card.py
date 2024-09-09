from siui.components.widgets import SiDenseHContainer, SiDenseVContainer, SiLabel
from siui.core.globals.globals import SiGlobal


class ABCSiOptionCardPlane(SiLabel):
    """
    Flat tabs, divided into [header, body, footer] to provide support for general scenarios
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spacing_ = 24

        # 构建组成外观的控件
        self.outfit_label_lower = SiLabel(self)
        self.outfit_label_lower.setFixedStyleSheet("border-radius: 6px")

        self.outfit_label_upper = SiLabel(self)
        self.outfit_label_upper.setFixedStyleSheet("border-radius: 6px")

        # 创建容器
        self.container = SiDenseVContainer(self)
        self.container.setSpacing(0)
        self.container.setAdjustWidgetsSize(True)

        # 创建划分区域
        self.header_ = SiDenseHContainer(self)
        self.header_.resize(0, 0)

        self.body_ = SiDenseVContainer(self)  # 只有 body 是竖直密堆积容器
        self.body_.setSpacing(8)
        self.body_.resize(0, 0)

        self.footer_ = SiDenseHContainer(self)
        self.footer_.resize(0, 0)

        # 设置子控件适应容器，并把三个组成部分添加到自己

        self.container.addWidget(self.header_)
        self.container.addWidget(self.body_)
        self.container.addWidget(self.footer_, "bottom")

    def setSpacing(self, spacing):
        """
        Set the spacing between the container and the left and right edges
        :param spacing: spacing
        """
        self.spacing_ = spacing

    def spacing(self):
        """
        Get the distance between the container and the left and right edges
        :return: spacing
        """
        return self.spacing_

    def header(self):
        """
        Returns the header container
        :return: Header container
        """
        return self.header_

    def body(self):
        """
        Returns the body container
        :return: body container
        """
        return self.body_

    def footer(self):
        """
        Return to the footer container
        :return: footer container
        """
        return self.footer_

    def adjustSize(self):
        self.resize(self.width(), self.header().height() + self.body().height() + self.footer().height() + 3)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.outfit_label_lower.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["INTERFACE_BG_A"]))
        self.outfit_label_upper.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["INTERFACE_BG_C"]))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.container.setGeometry(self.spacing(), 0, w-self.spacing()*2, h-3)

        self.outfit_label_lower.setGeometry(0, 8, w, h-8)  # 防止上边出现底色毛边
        self.outfit_label_upper.resize(w, h - 3)
