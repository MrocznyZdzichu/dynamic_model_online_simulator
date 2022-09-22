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
