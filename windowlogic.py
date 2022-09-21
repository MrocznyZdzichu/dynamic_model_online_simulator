from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
import sim_logic as sl
from singleton import Singleton
from PyQt5.QtCore import QTimer
pg.setConfigOption('background', (25, 35, 45))
pg.setConfigOption('foreground', 'w')


class Getter():
    def __init__(self, window):
        self.window = window

    def get_control_mode(self):
        tab_idx = self.window.tab_controllers.currentIndex()
        return self.window.tab_controllers.tabText(tab_idx)

    def get_manual_control_value(self):
        return float(self.window.le_man_cv.text())

    def get_push_button_start(self):
        return self.window.pb_start

    def get_push_button_stop(self):
        return self.window.pb_stop

    def get_push_button_clear(self):
        return self.window.pb_clear

    def get_cv_chart(self):
        return self.window.pg_cv

class Setter():
    def __init__(self, window):
        self.window = window

    def disable_element(self, gui_element):
        gui_element.setEnabled(False)

    def enable_element(self, gui_element):
        gui_element.setEnabled(True)

    def update_chart(self, chart, x, y):
        self.window.cv_line = chart.plot(x, y)


class GUI_Logic(QWidget, Singleton):
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
