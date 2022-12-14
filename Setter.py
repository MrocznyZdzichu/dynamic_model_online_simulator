class Setter():
    def __init__(self, window):
        self.window = window

    def disable_element(self, gui_element):
        gui_element.setEnabled(False)

    def enable_element(self, gui_element):
        gui_element.setEnabled(True)

    def update_chart(self, chart, x, y):
        self.window.cv_line = chart.plot(x, y)
