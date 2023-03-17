# from PyQt5.QtWidgets import QApplication, QLabel
# app = QApplication([])
# label = QLabel('Hello World!')
# label.show()
# app.exec_()

import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QSlider, QVBoxLayout, QWidget, QHBoxLayout)
from scipy import signal

# def window():
#     app = QApplication(sys.argv)
#     w = QWidget()
#     b = QLabel(w)
#     b.setText("Hello World!")
#     w.setGeometry(100,100,200,50)
#     b.move(50,20)
#     w.setWindowTitle("PyQt5")
#     w.show()
#     sys.exit(app.exec_())


# if __name__ == '__main__':
#     window()

class Color(QWidget):
    '''Find a color for the generated window.'''

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class SliderWithTitleAndValue(QWidget):
    """Custom Widget slider I created in order
    to have a title and an indication of the value.

    Args:
        QWidget (_type_): _description_
    """

    def __init__(self, title: str = 'Yet another slider',
                 min: int = 0, max: int = 20, init_val=1):

        super().__init__()
        self.setAutoFillBackground(True)
        hbox = QHBoxLayout()
        self.lblTitle = QLabel(title)
        self.slider = QSlider()
        self.slider.setRange(min, max)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        # self.slider.setMinimum(0)
        # self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.changedValue)
        self.lblValue = QLabel(str(init_val))
        # self.label.setFont(QtGui.QFont("Sanserif", 15))
        hbox.addWidget(self.lblTitle)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.lblValue)
        self.setLayout(hbox)

    def changedValue(self):
        size = self.slider.value()
        self.lblValue.setText(str(size))

    @property
    def value(self):
        return self.slider.value()


class App(QMainWindow):
    '''Main App class for interactive qt filter constructor.
    This is used to construct a window with sliders to
    finetune filters. At this point a butterworth with
    variable `filter order` '''

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        # Screen parameters
        self.left = 10
        self.top = 100
        self.width = 640
        self.height = 480
        self.init_ui()

    def init_ui(self):
        '''Initialize a window with the prefered geometry.'''
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Message in statusbar.')

        # add button
        btnPlotResponse = QPushButton('create Plot', self)
        btnPlotResponse.setToolTip('This is an example button')
        # button.move(100,70)
        btnPlotResponse.clicked.connect(self.on_click) 

        # # add slider
        # self.slFilterOrder = QSlider(Qt.Horizontal, self)
        # self.slFilterOrder.setGeometry(30, 40, 200, 30)
        # self.slFilterOrder.setRange(0, 100)
        # self.slFilterOrder.valueChanged[int].connect(self.changeFilterValue)
        # self.slFilterOrder.setFocusPolicy(Qt.StrongFocus)
        # self.slFilterOrder.setTickPosition(QSlider.TicksBothSides)
        # self.slFilterOrder.setTickInterval(10)
        # self.slFilterOrder.setSingleStep(1)

        #  Slider Label
        # self.lblFilterOrder = QLabel('0', self)

        # set my slider
        self.slFilterOrder_custom = SliderWithTitleAndValue(
            'Custom Silder', 0, 20, 1)


        # Add layout Chekc how to place object in a QtMainWindow
        main_layout = QVBoxLayout()
        main_layout.addWidget(btnPlotResponse)
        # mainLayout.addWidget(self.slFilterOrder)
        # mainLayout.addWidget(self.lblFilterOrder)
        main_layout.addWidget(self.slFilterOrder_custom)

        # Set mainLayout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.show()

    @pyqtSlot()
    def on_click(self):
        self.plot_gain_response()

    # @pyqtSlot()
    def changeFilterValue(self, value):
        # 4TH ORDER BUTTERWORTH FILTER WITH A GAIN DROP OF
        # 1/sqrt(2) AT 0.4 CYCLES/SAMPLE
        self.N = value
        self.lblFilterOrder.setText(str(value))

    def plot_gain_response(self):
        '''Plot the filter response.
        Create a plot with the filter coefficients.
        Until now only a small Butterworth IIR default is
        created from the given order'''

        self.N = self.slFilterOrder_custom.value
        bb, ab = signal.butter(self.N, 0.8, 'low',
                               analog=False, output='ba')
        print('Coefficients of b = ', bb)
        print('Coefficients of a = ', ab)
        wb, hb = signal.freqz(bb, ab)
        wb = wb/(2*math.pi)
        plt.plot(wb, abs(np.array(hb)))

        plt.title('Butterworth filter frequency response')
        plt.xlabel('Frequency [cycles/sample]')
        plt.ylabel('Amplitute [dB]')
        plt.margins(0, 0.1)
        plt.grid(which='both', axis='both')
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
