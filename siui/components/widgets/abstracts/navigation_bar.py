from PyQt5.QtCore import pyqtSignal

from siui.components.widgets.abstracts.widget import SiWidget


class ABCSiNavigationBar(SiWidget):
    """ Thanh điều hướng trừu tượng """
    indexChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 当前索引
        self.current_index_ = -1

        # 最大索引，需要最先设置
        self.maximum_index_ = -1

    def setCurrentIndex(self, index):
        """ Đặt chỉ mục hiện tại """
        self.current_index_ = index % (self.maximumIndex() + 1)
        self.indexChanged.emit(self.currentIndex())

    def currentIndex(self):
        """ Lấy chỉ mục hiện tại """
        return self.current_index_

    def setMaximumIndex(self, max_index):
        """ Đặt chỉ mục tối đa. Các chỉ mục vượt quá chỉ số tối đa sẽ được giữ lại. """
        if max_index < self.maximumIndex():
            self.maximum_index_ = max_index
            self.setCurrentIndex(self.currentIndex())  # 如果最大索引变小，这样可以防止其超过界限
        else:
            self.maximum_index_ = max_index

    def maximumIndex(self):
        """ Lấy chỉ số lớn nhất """
        return self.maximum_index_

    def shift(self, step: int):
        """
        Thêm chỉ mục hiện tại step
        :param step: step size
        """
        self.setCurrentIndex(self.currentIndex() + step)
