import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider, RangeSlider, Button, CheckButtons
import numpy as np
from scipy.signal import butter, filtfilt


class ControlPanel:
    def __init__(self, fig, side_bar_spec, redraw_callback):
        self.fig = fig
        self.redraw = redraw_callback  # функція для оновлення графіка
        self.sliders = {}
        self.axes = {}
        self.buildUI(side_bar_spec)

    def buildUI(self, side_bar):
        options = side_bar.subgridspec(9, 1)
        slider_settings = {
            'Amplitude': (0.1, 5, 1),
            'Frequency': (1, 10, 2),
            'Phase': (0, 2 * np.pi, 0),
            'Noise Mean': (-2, 2, 0),
            'Noise Cov.': (0, 1, 0.25)
        }

        for i, (name, (vmin, vmax, vdef)) in enumerate(slider_settings.items()):
            self.axes[name] = self.fig.add_subplot(options[i])
            self.sliders[name] = Slider(self.axes[name], name, vmin, vmax, valinit=vdef)
            is_noise = name not in ['Amplitude', 'Frequency', 'Phase']
            self.sliders[name].on_changed(lambda val , is_n = is_noise: self.redraw(is_n))

        self.axes['Cutoff Freq'] = self.fig.add_subplot(options[5])
        self.sliders['Cutoff Freq'] = RangeSlider(self.axes['Cutoff Freq'], 'Cutoff Freq', 0.01, 50, valinit=(0.5, 2))
        self.sliders['Cutoff Freq'].on_changed(lambda val: self.redraw(False))

        self.axes['Show Noise'] = self.fig.add_subplot(options[6])
        self.ShowNoise = CheckButtons(self.axes['Show Noise'], ['Show Noise'], [True])
        self.ShowNoise.on_clicked(lambda label: self.redraw(False))

        self.axes['Show Filter'] = self.fig.add_subplot(options[7])
        self.ShowFilter = CheckButtons(self.axes['Show Filter'], ['Show Filter'], [True])
        self.ShowFilter.on_clicked(lambda label: self.redraw(False))

        self.axes['Reset'] = self.fig.add_subplot(options[8])
        self.Reset = Button(self.axes['Reset'], 'Reset')
        self.Reset.on_clicked(self.resetSliders)

    def resetSliders(self, event=None):
        for name, sl in self.sliders.items():
            if hasattr(sl, 'reset'):
                sl.reset()
            elif isinstance(sl, RangeSlider):
                sl.set_val((0.1, 75))

def mainWindow():
    fig = plt.figure(figsize=(12, 4))
    outer = GridSpec(ncols=2, nrows=1, figure=fig, width_ratios=[3, 2], wspace=0.3)

    # Додає графік
    ax_plot = fig.add_subplot(outer[0, 0])

    line_signal = None
    line_noise = None
    line_filtered = None
    noise_data = None
    # Функція оновлення графіка
    def draw_plot(redraw_noise):
        nonlocal line_signal, line_noise, line_filtered, noise_data

        t = np.linspace(0, 1, 500)
        A = control.sliders['Amplitude'].val
        f = control.sliders['Frequency'].val
        phi = control.sliders['Phase'].val
        y = A * np.sin(2 * np.pi * f * t + phi)

        #оця частина намалює нову гармоніку якшо її нема, або змінить існуючу
        if line_signal is None:
            line_signal, = ax_plot.plot(t, y, label='Signal')
        else:
            line_signal.set_ydata(y)

        if not redraw_noise:
            ax_plot.autoscale_view()

        #згенерує і збереже шум
        if redraw_noise or noise_data is None:
            mean = control.sliders['Noise Mean'].val
            cov = control.sliders['Noise Cov.'].val
            noise_data = np.random.normal(mean, cov, size=t.shape)
        #якшо шум не помінявся, то на графіку відобразиться старий, враховуючи новий у
        y_noise = y + noise_data


        #ця частина відобразить шум
        if control.ShowNoise.get_status()[0]:
            if line_noise is not None:
                line_noise.set_ydata(y_noise)
            else:
                line_noise, = ax_plot.plot(t, y_noise, label='Signal + Noise', alpha=0.5, color='pink')
        else:
            if line_noise is not None:
                line_noise.remove()
                line_noise = None

        #створить і відобразить відфільтровану частину
        if control.ShowFilter.get_status()[0]:
            low, high = control.sliders['Cutoff Freq'].val
            b, a = butter(N=4, Wn=(low, high), btype='band', fs=500)
            filtered = filtfilt(b, a, y_noise)

            if line_filtered is None:
                line_filtered, = ax_plot.plot(t, filtered, label='Filtered', color='purple')
            else:
                line_filtered.set_ydata(filtered)

        else:
            if line_filtered is not None:
                line_filtered.remove()
                line_filtered = None

        ax_plot.relim()
        ax_plot.legend()
        fig.canvas.draw_idle()

    # Панель керування, передаємо redraw
    control = ControlPanel(fig, outer[0, 1], redraw_callback=draw_plot)

    draw_plot(True)  # перший малюнок
    plt.show()


if __name__ == '__main__':
    mainWindow()
