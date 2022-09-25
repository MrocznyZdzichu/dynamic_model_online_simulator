class Getter():
    def __init__(self, window):
        self.window = window

    def get_control_mode(self):
        tab_idx = self.window.tab_controllers.currentIndex()
        return self.window.tab_controllers.tabText(tab_idx)

    def get_model_type(self):
        tab_idx = self.window.tab_plants.currentIndex()
        return self.window.tab_plants.tabText(tab_idx)

    def get_manual_control_value(self):
        return float(self.window.le_man_cv.text())

    def get_push_button_start(self):
        return self.window.pb_start

    def get_push_button_stop(self):
        return self.window.pb_stop

    def get_push_button_clear(self):
        return self.window.pb_clear

    def get_push_button_update_tf(self):
        return self.window.pb_up_tf

    def get_cv_chart(self):
        return self.window.pg_cv

    def get_sp_pv_chart(self):
        return self.window.pg_sp_pv

    def get_numerator(self):
        input_text = self.window.le_tf_num.text()
        input_as_list = [float(numerator) for numerator in input_text.split(' ')]
        return input_as_list

    def get_denominator(self):
        input_text = self.window.le_tf_den.text()
        input_as_list = [float(denominator) for denominator in input_text.split(' ')]
        return input_as_list

    def get_kd(self):
        return float(self.window.le_kd.text())

    def get_ki(self):
        return float(self.window.le_ki.text())

    def get_kp(self):
        return float(self.window.le_kp.text())

    def get_pid_mode(self):
        return self.window.cb_pid_mode.currentText()

    def get_pid_sp(self):
        return float(self.window.le_pid_sp.text())

    def get_pid_ymin(self):
        return float(self.window.le_pid_ymin.text())

    def get_pid_ymax(self):
        return float(self.window.le_pid_ymax.text())
