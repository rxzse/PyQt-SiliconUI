import time

import numpy
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QPushButton

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiLabel
from siui.core.animation import SiExpAnimation
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.gui.color_group import SiColorGroup


class ABCButton(QPushButton):
    """
    Abstract button control\n
    Provide click, press, release signals and color animations
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setStyleSheet("background-color: transparent")

        self.hint = ""
        self.color_group = SiColorGroup(reference=SiGlobal.siui.colors)
        self.flash_on_clicked = True
        self.enabled_repetitive_clicking = False

        self.attachment_ = SiWidget()                       # 占位用的被绑定部件，显示在按钮正中央
        self.attachment_shifting = numpy.array([0, 0])      # 被绑定部件偏离中心的像素数

        # 提供悬停时的颜色变化动画
        self.hover_highlight = SiLabel(self)
        self.hover_highlight.stackUnder(self)  # 置于按钮的底部
        self.hover_highlight.setColor(SiColor.trans(self.colorGroup().fromToken(SiColor.BUTTON_HOVER), 0.0))
        self.hover_highlight.animationGroup().fromToken("color").setBias(0.2)
        self.hover_highlight.animationGroup().fromToken("color").setFactor(1 / 8)

        # 提供点击时的颜色变化动画
        self.flash_label = SiLabel(self)
        self.flash_label.stackUnder(self)  # 置于按钮的底部
        self.flash_label.setColor(SiColor.trans(self.colorGroup().fromToken(SiColor.BUTTON_FLASH), 0.0))
        self.flash_label.animationGroup().fromToken("color").setBias(0.2)
        self.flash_label.animationGroup().fromToken("color").setFactor(1 / 8)

        self.clicked.connect(self._on_self_clicked)

        self.repeat_clicking_timer = QTimer(self)
        self.repeat_clicking_timer.setInterval(50)
        self.repeat_clicking_timer.timeout.connect(self.clicked.emit)

        self.repeat_clicking_trigger_timer = QTimer(self)
        self.repeat_clicking_trigger_timer.setSingleShot(True)
        self.repeat_clicking_trigger_timer.timeout.connect(self.repeat_clicking_timer.start)
        self.repeat_clicking_trigger_timer.setInterval(500)

    def setAttachmentShifting(self, x, y):
        """
        Set the number of pixels that the bound component deviates from the center. 
        The offset will be directly added to its coordinates as the final position
        :param x: How many pixels does the horizontal axis shift?
        :param y: How many pixels to offset the vertical axis
        :return:
        """
        self.attachment_shifting = numpy.array([x, y])

    def setAttachment(self, widget):
        """
        Set the binding component. The binding component will be set as a subcontrol of the button and displayed in the center of the button
        :param widget: widget
        """
        # 删除旧的绑定部件
        self.attachment_.deleteLater()

        self.attachment_ = widget
        self.attachment_.setParent(self)
        self.resize(self.size())  # 实现刷新位置

    def attachment(self):
        """
        Returns the bound component
        :return: Bound components
        """
        return self.attachment_

    def colorGroup(self):
        """
        Get the color group of this widget
        :return: SiColorGroup
        """
        return self.color_group

    def setHint(self, text: str):
        """
        Setting Tooltips
        :param text: content
        :return:
        """
        self.hint = text

    def setRepetitiveClicking(self, state):
        self.enabled_repetitive_clicking = state

    def setFixedStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        Set the button component's fixed style sheet\n
        Note that this will not set the fixed style sheet of the button itself,\n
        and cannot change the corresponding color settings.\n
        This method should only be used to change properties such as border radius.
        :param style_sheet: Fixed style sheet
        :return:
        """
        self.hover_highlight.setFixedStyleSheet(style_sheet)
        self.flash_label.setFixedStyleSheet(style_sheet)

    def setStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        """
        Set the button component style sheet\n
        Note that this will not set the style sheet of the button itself,\n
        and will not change the corresponding color settings.\n
        This method should only be used to change properties such as border radius.
        :param style_sheet: Style Sheets
        :return:
        """
        self.hover_highlight.setStyleSheet(style_sheet)
        self.flash_label.setStyleSheet(style_sheet)

    def reloadStyleSheet(self):
        """
        Overload the style sheet.\n
        It is recommended to rewrite all the contents of the style sheet in this method.\n
        This method is called when the window show method is called or the theme is changed.
        :return:
        """
        self.attachment().reloadStyleSheet()
        return

    def flashLabel(self):
        """ get the label that preform flashing animations """
        return self.flash_label

    def hoverLabel(self):
        """ get the hover-highlight label """
        return self.hover_highlight

    def setFlashOnClicked(self, b: bool):
        """
        Set whether to enable click animation
        :param b: boolean
        :return:
        """
        self.flash_on_clicked = b

    def _on_self_clicked(self):
        if self.flash_on_clicked is True:
            self._run_clicked_ani()

    def _run_clicked_ani(self):
        self.flash_label.setColor(self.color_group.fromToken(SiColor.BUTTON_FLASH))
        self.flash_label.setColorTo(SiColor.trans(self.color_group.fromToken(SiColor.BUTTON_FLASH), 0))

    def flash(self):
        """ play flash animation once but do nothing else """
        self._run_clicked_ani()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo(self.color_group.fromToken(SiColor.BUTTON_HOVER))

        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(self)
            SiGlobal.siui.windows["TOOL_TIP"].show_()
            SiGlobal.siui.windows["TOOL_TIP"].setText(self.hint)

    def leaveEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo(SiColor.trans(self.color_group.fromToken(SiColor.BUTTON_HOVER), 0))

        if self.hint != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(None)
            SiGlobal.siui.windows["TOOL_TIP"].hide_()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if self.enabled_repetitive_clicking:
            self.repeat_clicking_trigger_timer.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.repeat_clicking_trigger_timer.stop()
        self.repeat_clicking_timer.stop()

    def adjustSize(self):
        """
        Adjust the size of the button according to the size of the bound control
        :return:
        """
        att_size = self.attachment().size()
        preferred_width = max(32, att_size.width() + 24)
        preferred_height = max(32, att_size.height() + 8)

        self.resize(preferred_width, preferred_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.hover_highlight.resize(size)
        self.flash_label.resize(size)

        self.attachment_.move((w - self.attachment_.width()) // 2 + self.attachment_shifting[0],
                              (h - self.attachment_.height()) // 2 + self.attachment_shifting[1])


class ABCPushButton(ABCButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 按钮表面
        self.body_top = SiLabel(self)
        self.body_top.lower()

        # 绘制最底层阴影部分
        self.body_bottom = SiLabel(self)
        self.body_bottom.lower()

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 设置按钮表面的圆角边框
        self.body_top.setFixedStyleSheet("""
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
        """)

        # 设置按钮阴影的圆角边框
        self.body_bottom.setFixedStyleSheet("border-radius: 4px")

        # 把有效区域设置成 PushButton 的形状
        self.setFixedStyleSheet("""
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.hover_highlight.resize(w, h - 3)
        self.flash_label.resize(w, h - 3)

        self.body_top.resize(w, h - 3)
        self.body_bottom.resize(w, h)


class LongPressThread(QThread):
    """
    The thread for long pressing the button is used to handle long pressing timing, signal triggering and animation
    """
    ticked = pyqtSignal(float)
    holdTimeout = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_ = parent

        # 创建一个动画，不激活动画，而是每次运行时调用一次_process方法
        self.animation = SiExpAnimation(self)
        self.animation.setCurrent(0)
        self.animation.setTarget(1)
        self.animation.setBias(0.001)
        self.animation.setFactor(1 / 16)
        self.animation.ticked.connect(self.ticked.emit)

    def parent(self):
        return self.parent_

    # 重写进程
    def run(self):
        # 初始化等待时间
        time_start_waiting = time.time()

        # 前进动画
        while time.time() - time_start_waiting <= 0.5:  # 即便松开，在额定时间内继续按压仍然会继续计数

            # 如果父对象按钮处于按下状态并且动画尚未完成
            while self.parent().isPressed() and self.animation.current() < 1:
                # 重置等待时间
                time_start_waiting = time.time()

                # 更新进度并发射信号
                self.animation._process()

                # 等待帧
                time.sleep(1 / 60)

            # 如果循环被跳出，并且此时动画已经完成了
            if self.animation.current() == 1:
                # 发射长按已经超时信号，即此时点击已经被确认
                self.holdTimeout.emit()

                # 让进度停留一会，并跳出前进动画循环
                time.sleep(10 / 60)
                break

            time.sleep(1 / 60)

        # 如果前进的循环已经被跳出，并且此时动画进度不为0
        while self.animation.current() > 0:
            # 减少动画进度，直至0，并不断发射值改变信号
            self.animation.setCurrent(max(0, self.animation.current() - 0.1))
            self.animation.ticked.emit(self.animation.current())
            time.sleep(1 / 60)


class ABCToggleButton(ABCButton):
    """
    Toggle button abstract class, note: this is not the abstract class of the check box
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 圆角半径
        self.border_radius = 4

        # 设置自己为可选中
        self.setCheckable(True)

        # 创建一个颜色叠层，用于标识被选中的状态
        self.color_label = SiLabel(self)
        self.color_label.setColor(self.colorGroup().fromToken(SiColor.BUTTON_OFF))  # 初始是关闭状态

        # 把状态切换信号绑定到颜色切换的槽函数上
        self.toggled.connect(self._toggled_handler)

        # 闪光和悬停置顶，防止设定不透明颜色时没有闪光
        self.hover_highlight.raise_()
        self.flash_label.raise_()

    def colorLabel(self):
        return self.color_label

    def setBorderRadius(self, r: int):
        """
        Set the border corner radius
        :param r: int
        """
        self.border_radius = r

    def reloadStyleSheet(self):
        # 设置颜色块圆角
        self.color_label.setFixedStyleSheet(f"border-radius: {self.border_radius}px")

        # 设置自身圆角
        self.setFixedStyleSheet(f"border-radius: {self.border_radius}px")

        # 刷新颜色
        self.color_label.setColor(self.colorGroup().fromToken(SiColor.BUTTON_ON if self.isChecked() else SiColor.BUTTON_OFF))  # noqa: E501

    def _toggled_handler(self, state):
        if state is True:
            self.color_label.setColorTo(self.colorGroup().fromToken(SiColor.BUTTON_ON))
        else:
            self.color_label.setColorTo(self.colorGroup().fromToken(SiColor.BUTTON_OFF))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.color_label.resize(event.size())
