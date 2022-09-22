from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
pg.setConfigOption('background', (25, 35, 45))
pg.setConfigOption('foreground', 'w')

from Setter import Setter
from Getter import Getter


class GUI_Logic(QWidget):
    def __init__(self, window):
        super().__init__()
        self.getter = Getter(window)
        self.setter = Setter(window)
        self.window_handle = window

        self.timestamps = [0]
        self.cvs = [0]

        self.setter.disable_element(self.getter.get_push_button_stop())
        self.setter.disable_element(self.getter.get_push_button_clear())

    def connect_signals(self):
        self.window_handle.pb_start.clicked.connect(self.slot_start_sim)
        self.window_handle.pb_stop.clicked.connect(self.slot_pause_sim)
        self.window_handle.pb_clear.clicked.connect(self.slot_clear_sim)

    def slot_start_sim(self):
        self.mode = self.getter.get_control_mode()

        self.timer = QTimer()
        self.configure_timer()
        self.timer.start(100)

        self.setter.disable_element(self.getter.get_push_button_start())
        self.setter.disable_element(self.getter.get_push_button_clear())
        self.setter.enable_element(self.getter.get_push_button_stop())

    def configure_timer(self):
        self.timer.timeout.connect(self.append_timestamps)
        self.timer.timeout.connect(self.get_current_state)
        self.timer.timeout.connect(self.sim_step)
        self.timer.timeout.connect(lambda: self.setter.update_chart(self.getter.get_cv_chart(),
                                                                    self.timestamps,
                                                                    self.cvs))

    def append_timestamps(self):
        self.timestamps.append(self.timestamps[-1]+0.1)

    def get_current_state(self):
        self.curr_man_cv = self.getter.get_manual_control_value()

    def sim_step(self):
        if self.mode == 'Manual Control':
            self.manual_sim()

    def manual_sim(self):
        curr_CV = self.getter.get_manual_control_value()
        self.cvs.append(curr_CV)

    def slot_pause_sim(self):
        self.timer.stop()
        self.setter.disable_element(self.getter.get_push_button_stop())
        self.setter.enable_element(self.getter.get_push_button_start())
        self.setter.enable_element(self.getter.get_push_button_clear())

    def slot_clear_sim(self):
        self.cvs = [0]
        self.timestamps = [0]
        self.setter.disable_element(self.getter.get_push_button_clear())
        self.getter.get_cv_chart().clear()
