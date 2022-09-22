from Setter import Setter
from Getter import Getter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import scipy.signal as sp
pg.setConfigOption('background', (25, 35, 45))
pg.setConfigOption('foreground', 'w')


class GUI_Logic(QWidget):
    def __init__(self, window):
        super().__init__()
        self.getter = Getter(window)
        self.setter = Setter(window)
        self.window_handle = window

        self.timestamps = [0]
        self.cvs = [0]
        self.ys = [0]

        self.setter.disable_element(self.getter.get_push_button_start())
        self.setter.disable_element(self.getter.get_push_button_stop())
        self.setter.disable_element(self.getter.get_push_button_clear())

    def connect_signals(self):
        self.window_handle.pb_start.clicked.connect(self.slot_start_sim)
        self.window_handle.pb_stop.clicked.connect(self.slot_pause_sim)
        self.window_handle.pb_clear.clicked.connect(self.slot_clear_sim)

        self.window_handle.pb_up_tf.clicked.connect(self.update_tf_model)

    def slot_start_sim(self):
        self.mode = self.getter.get_control_mode()
        self.type = self.getter.get_model_type()

        self.timer = QTimer()
        self.configure_timer()
        self.timer.start(100)

        self.setter.disable_element(self.getter.get_push_button_start())
        self.setter.disable_element(self.getter.get_push_button_clear())
        self.setter.disable_element(self.getter.get_push_button_update_tf())
        self.setter.enable_element(self.getter.get_push_button_stop())

    def configure_timer(self):
        self.timer.timeout.connect(self.append_timestamps)
        self.timer.timeout.connect(self.get_current_state)
        self.timer.timeout.connect(self.sim_step)
        self.timer.timeout.connect(lambda: self.setter.update_chart(self.getter.get_cv_chart(),
                                                                    self.timestamps,
                                                                    self.cvs))
        self.timer.timeout.connect(lambda: self.setter.update_chart(self.getter.get_sp_pv_chart(),
                                                                   self.timestamps,
                                                                   self.ys))

    def append_timestamps(self):
        self.timestamps.append(self.timestamps[-1]+0.1)

    def get_current_state(self):
        self.curr_man_cv = self.getter.get_manual_control_value()

    def sim_step(self):
        self.cvs.append(self.compute_cv(self.mode))
        self.ys.append(self.compute_output(self.type))

    def compute_cv(self, cv_mode):
        if cv_mode == 'Manual Control':
            curr_CV = self.getter.get_manual_control_value()
            return curr_CV

    def compute_output(self, model_type):
        if model_type == 'Transfer Function':
            times, output, state_vector = sp.lsim(self.plant, self.cvs, self.timestamps)
            return output[-1]

    def slot_pause_sim(self):
        self.timer.stop()
        self.setter.disable_element(self.getter.get_push_button_stop())
        self.setter.enable_element(self.getter.get_push_button_start())
        self.setter.enable_element(self.getter.get_push_button_clear())
        self.setter.enable_element(self.getter.get_push_button_update_tf())

    def slot_clear_sim(self):
        self.cvs = [0]
        self.timestamps = [0]
        self.ys = [0]

        self.setter.disable_element(self.getter.get_push_button_clear())
        self.getter.get_sp_pv_chart().clear()
        self.getter.get_cv_chart().clear()

    def update_tf_model(self):
        numerator = self.getter.get_numerator()
        denominator = self.getter.get_denominator()

        self.plant = sp.TransferFunction(numerator, denominator)

        self.setter.disable_element(self.getter.get_push_button_update_tf())
        self.setter.enable_element(self.getter.get_push_button_start())
