"""
tooltip 模块
实现工具提示
"""
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.label import SiLabel
from siui.core.globals import SiGlobal
from siui.gui.font import GlobalFont, SiFont
from siui.core.silicon import Si


class ToolTipWindow(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.completely_hid = False  # 是否已经完全隐藏（透明度是不是0）
        self.animationGroup().fromToken("opacity").finished.connect(self._completely_hid_signal_handler)

        self.margin = 8  # 周围给阴影预留的间隔空间
        self.shadow_size = 8  # 阴影

        self.now_inside_of = None  # 在哪个控件内部（最近一次被谁触发过显示事件）

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 128))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(int(self.shadow_size * 1.5))
        self.setGraphicsEffect(shadow)

        # 跟踪鼠标的计时器，总处于启动状态
        self.tracker_timer = QTimer()
        self.tracker_timer.setInterval(int(1000/60))
        self.tracker_timer.timeout.connect(self._refresh_position)
        self.tracker_timer.start()

        # 背景颜色，可以用于呈现不同类型的信息
        self.bg_label = SiLabel(self)
        self.bg_label.move(self.margin, self.margin)
        self.bg_label.setFixedStyleSheet("border-radius: 6px")

        # 文字标签的父对象，防止文字超出界限
        self.text_container = SiLabel(self)
        self.text_container.move(self.margin, self.margin)

        # 文字标签，工具提示就在这里显示，
        self.text_label = SiLabel(self.text_container)
        self.text_label.setFixedStyleSheet("padding: 8px")
        self.text_label.setSiliconWidgetFlag(Si.InstantResize)
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.text_label.setFont(SiFont.fromToken(GlobalFont.S_NORMAL))

        # 高光遮罩，当信息刷新时会闪烁一下
        self.highlight_mask = SiLabel(self)
        self.highlight_mask.move(self.margin, self.margin)
        self.highlight_mask.setFixedStyleSheet("border-radius: 6px")
        self.highlight_mask.setColor("#00FFFFFF")

        # 通过输入空文本初始化大小
        self.setText("", flash=False)

    def reloadStyleSheet(self):
        self.bg_label.setColor(SiGlobal.siui.colors["TOOLTIP_BG"])
        self.text_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))

    def show_(self):
        self.setOpacityTo(1.0)

    def hide_(self):
        self.setOpacityTo(0)

    def _completely_hid_signal_handler(self, target):
        if target == 0:
            self.completely_hid = True
            self.resize(2 * self.margin, 36 + 2 * self.margin)  # 变单行内容的高度，宽度不足以显示任何内容
            self.text_label.setText("")   # 清空文本内容

    def setNowInsideOf(self, widget):
        """
        Sets which control is currently inside. For siui controls, 
        this will be called and passed in the caller when setting 
        the tooltip to be displayed, and will be called and passed in 
        [None] when it is hidden
        :param widget: Inside which control (who triggered the display)
        :return:
        """
        self.now_inside_of = widget

    def nowInsideOf(self):
        """
        Returns the issuer of the last call to display
        :return: Control|None
        """
        return self.now_inside_of

    def setText(self, text, flash=True):
        """
        Set the tooltip content, support rich text
        :param text: Content, which will be converted into a string
        :param flash: Whether to flash the highlight layer
        :return:
        """
        text_changed = self.text_label.text() != text
        self.text_label.setText(str(text))
        self._refresh_size()
        if flash and text_changed:
            self.flash()

    def _refresh_size(self):
        """
        Used to set the end value of the size animation and start the animation
        :return:
        """
        w, h = self.text_label.width(), self.text_label.height()

        # 让自身大小变为文字标签的大小加上阴影间距
        self.resizeTo(w + 2 * self.margin, h + 2 * self.margin)

    def flash(self):
        """
        Activate the highlight layer animation to make the highlight layer flash
        :return:
        """
        # 刷新高亮层动画当前值和结束值，实现闪烁效果
        self.highlight_mask.setColor("7FFFFFFF")
        self.highlight_mask.setColorTo("#00FFFFFF")

    def _refresh_position(self):
        pos = QCursor.pos()
        x, y = pos.x(), pos.y()
        # self.move(x, y)
        self.moveTo(x + 4, y - self.height())    # 动画跟踪，效果更佳，有了锚点直接输入鼠标坐标即可

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width() - 2 * self.margin, size.height() - 2 * self.margin

        # 重设内部控件大小
        self.bg_label.resize(w, h)
        self.text_container.resize(w, h)
        self.highlight_mask.resize(w, h)

        # 移动文本位置，阻止重设大小动画进行时奇怪的文字移动
        self.text_label.move(0, h - self.text_label.height())

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()
