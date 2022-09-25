from Setter import Setter
from Getter import Getter
from DB_Logger import DB_Logger
import utils
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import *
import pyqtgraph as pg
from simple_pid import PID
import scipy.signal as sp
pg.setConfigOption('background', (25, 35, 45))
pg.setConfigOption('foreground', 'w')


class GUI_Logic(QWidget):
    def __init__(self, window):
        super().__init__()
        self.getter = Getter(window)
        self.setter = Setter(window)
        self.window_handle = window
        self.connect_signals()
        self.logger = DB_Logger()

        self.timestamps = [0]
        self.cvs = [0]
        self.ys = [0]
        self.sp = [0]

        self.setter.disable_element(self.getter.get_push_button_start())
        self.setter.disable_element(self.getter.get_push_button_stop())
        self.setter.disable_element(self.getter.get_push_button_clear())

    def connect_signals(self):
        self.window_handle.pb_start.clicked.connect(self.slot_start_sim)
        self.window_handle.pb_stop.clicked.connect(self.slot_pause_sim)
        self.window_handle.pb_clear.clicked.connect(self.slot_clear_sim)

        self.window_handle.pb_up_tf.clicked.connect(self.update_tf_model)
        self.window_handle.pb_create_pid.clicked.connect(self.build_pid_controller)

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

        self.getter.get_cv_chart().addLegend()
        self.getter.get_sp_pv_chart().addLegend()

    def configure_timer(self):
        self.timer.timeout.connect(self.append_timestamps)
        self.timer.timeout.connect(self.get_current_state)
        self.timer.timeout.connect(self.sim_step)
        self.timer.timeout.connect(lambda: self.setter.update_chart(self.getter.get_cv_chart(),
                                                                    self.timestamps,
                                                                    [self.cvs],
                                                                    [{'name' : 'Control Value'}]))

        self.timer.timeout.connect(lambda: self.setter.update_chart(self.getter.get_sp_pv_chart(),
                                                                    self.timestamps,
                                                                   (    self.ys, self.sp),
                                                                        [
                                                                            {'name' : 'Process Value'}
                                                                            ,{'name' : 'Set Point'
                                                                            ,'pen' : pg.mkPen(color=(0, 0, 200), width=1, style=Qt.DashLine)}
                                                                        ]
                                                                    ))

    def append_timestamps(self):
        self.timestamps.append(self.timestamps[-1]+0.1)

    def get_current_state(self):
        if self.mode == 'Manual Control':
            self.curr_man_cv = self.getter.get_manual_control_value()
        elif self.mode == 'PID Controller':
            self.curr_sp = self.getter.get_pid_sp()

    def sim_step(self):
        self.sp.append(self.get_sp(self.mode))
        self.cvs.append(self.compute_cv(self.mode))
        self.ys.append(self.compute_output(self.type))

        self.logger.log_sim_step(self.build_state_dict())

    def compute_cv(self, cv_mode):
        if cv_mode == 'Manual Control':
            curr_CV = self.getter.get_manual_control_value()

        elif cv_mode == 'PID Controller':
            self.pid.setpoint = self.curr_sp
            curr_CV = self.pid(self.ys[-1])

        return curr_CV

    def compute_output(self, model_type):
        if model_type == 'Transfer Function':
            times, output, state_vector = sp.lsim(self.plant, self.cvs, self.timestamps)
            return output[-1]

    def get_sp(self, mode):
        if mode == 'Manual Control':
            return self.compute_static_gain()
        elif mode == 'PID Controller':
            return self.getter.get_pid_sp()
        else:
            return 0

    def compute_static_gain(self):
        if self.type == 'Transfer Function':
            if self.denominator[-1] != 0:
                gain = self.numerator[-1]/self.denominator[-1] * self.curr_man_cv
            else:
                gain = 0
        return gain

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
        self.sp = [0]

        self.setter.disable_element(self.getter.get_push_button_clear())
        self.getter.get_sp_pv_chart().clear()
        self.getter.get_cv_chart().clear()

    def update_tf_model(self):
        self.numerator = self.getter.get_numerator()
        self.denominator = self.getter.get_denominator()

        self.plant = sp.TransferFunction(self.numerator, self.denominator)

        self.setter.disable_element(self.getter.get_push_button_update_tf())
        self.setter.enable_element(self.getter.get_push_button_start())

    def build_state_dict(self):
        state = {
            'LOG_DTTM' : 'SYSDATE'
            , 'SIM_MODE' : f"'{self.mode}'"
            , 'PLANT_TYPE' : f"'{self.type}'"
            , 'SIM_TIME' : round(self.timestamps[-1], 1)
            , 'CV' : round(self.cvs[-1], 3)
            , 'PV' : round(self.ys[-1], 3)
            , 'SP' : round(self.sp[-1], 3)
            , 'PLANT_DESC' : f"'{self.build_plant_desc()}'"
            , 'REGULATOR_DESC' : f"'{self.build_regulator_desc()}'"
        }
        return state

    def build_plant_desc(self):
        if self.type == 'Transfer Function':
            num_str = utils.tf_human_readable(self.getter.get_numerator())
            den_str = utils.tf_human_readable(self.getter.get_denominator())
            return f'({num_str})/({den_str})'

    def build_regulator_desc(self):
        if self.mode == 'Manual Control':
            reg_desc = 'No regulator, set point computed as X * static gain'
        elif self.mode == 'PID Controller':
            reg_desc = \
        f"PID Controller: P = {self.kp}, I = {self.ki}, D = {self.kp}, bounds = ({self.pid_ymin}, {self.pid_ymax})"
        return reg_desc

    def build_pid_controller(self):
        self.pid_mode = self.getter.get_pid_mode()

        self.kp = self.getter.get_kp() if self.pid_mode == 'Simple' \
                                        else -1*self.getter.get_kp()
        self.ki = self.getter.get_ki() if self.pid_mode == 'Simple' \
                                        else -1*self.getter.get_ki()
        self.kd = self.getter.get_kd() if self.pid_mode == 'Simple' \
                                        else -1*self.getter.get_kd()

        self.pid_ymin = self.getter.get_pid_ymin()
        self.pid_ymax = self.getter.get_pid_ymax()

        self.pid = PID(self.kp, self.ki, self.kd
                      , sample_time = 0.1)
        self.pid.output_limits = (self.pid_ymin, self.pid_ymax)
