import utils


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
        return utils.get_le_as_float(self.window.le_man_cv)

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
        return utils.get_le_as_list_of_floats(self.window.le_tf_num)

    def get_denominator(self):
        return utils.get_le_as_list_of_floats(self.window.le_tf_den)

    def get_kd(self):
        return utils.get_le_as_float(self.window.le_kd)

    def get_ki(self):
        return utils.get_le_as_float(self.window.le_ki)

    def get_kp(self):
        return utils.get_le_as_float(self.window.le_kp)

    def get_pid_mode(self):
        return self.window.cb_pid_mode.currentText()

    def get_pid_sp(self):
        return utils.get_le_as_float(self.window.le_pid_sp)

    def get_pid_ymin(self):
        return utils.get_le_as_float(self.window.le_pid_ymin)

    def get_pid_ymax(self):
        return utils.get_le_as_float(self.window.le_pid_ymax)
