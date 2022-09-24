from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from PyQt5 import uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import windowlogic as WL
import qdarkstyle
from windowlogic import GUI_Logic


class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        window = uic.loadUi('mainwindow.ui', self)
        window.show()

# create pyqt5 app
App = QApplication(sys.argv)
App.setStyleSheet(qdarkstyle.load_stylesheet())
# create the instance of our Window
window = Window()
logic = GUI_Logic(window)
# start the app
sys.exit(App.exec())
