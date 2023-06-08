import osc_conf as HANDLER
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# matplotlib.use('Qt5Agg') # set up this backend on OPI

plt.rcParams['toolbar'] = 'None'

class OSC:
    def __init__(self, data, figsize=(14, 4)):
        self.animation = None
        self.ADC = data
        self.INTERVAL = 60          # frame animation interval in millisec
        self.SCROLL_TIME = 64
        self.THRESHOLD = 0.5
        self.CHAOS_PERF_TIME = 4    # time of chaotic performance in sec.
        self.RESTART_TIME = 2       # time of restart performance in sec.
        self.BACK = matplotlib.get_backend()

        # Initialize the figure and axis
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.fig.set_facecolor('black')
        self.fig.canvas.manager.set_window_title('Chaotic System 1')
        self.ax.set_facecolor('black')
        self.ax.spines[:].set_color('black')
        self.ax.tick_params(axis='x', colors='white', labelsize=6)
        self.ax.tick_params(axis='y', colors='white', labelsize=6)

        # Set the limits of the x and y axes to zoom out
        self.ax.set_ylim(-0.5, 3)
        plt.subplots_adjust(left=0.18, right=0.96)

        # Initialize the lines
        self.LINEW = 2
        self.line1, = self.ax.plot([], [], linewidth=self.LINEW, label='Generator A')
        self.line2, = self.ax.plot([], [], linewidth=self.LINEW, label='Generator B')

        # Legend, text, labels and timers
        self.legend = plt.legend(loc='center right', bbox_to_anchor=(-0.05, 0.96),
                                 facecolor='black', edgecolor='black', labelcolor='white')

        self.txt_blocks = {}                # dict for text blocks to change them later
        self.timers_default = '00:00:000'
        self.text_prop = HANDLER.text_prop          # from config
        self.text_block_prop = HANDLER.osc_blocks   # from config
        self.decoration = HANDLER.line_decoration   # from config
        for key in self.text_block_prop.keys():
            self.draw_txt_blocks(key)

    def draw_txt_blocks(self, block_name):
        txt_p = self.text_prop
        blck_p = self.text_block_prop.get(block_name, {})

        inner_txt = blck_p.get('innertxt', '<txt>')
        fsize = blck_p.get('fontsize', 10)
        padding_left = blck_p.get('padding_left', 0)
        padding_bottom = blck_p.get('padding_bottom', 0)
        horiz_alg = blck_p.get('horizontalalignment', 'right')
        color = blck_p.get('color', 'white')

        txt_block = self.fig.text(
            padding_left, padding_bottom, inner_txt, ha=horiz_alg, color=color, fontsize=fsize, **txt_p)
        self.txt_blocks[block_name] = txt_block # save dict with blocks
        return txt_block

    def chaos_enabler(self):    # if chaos started self._is_chaos_decorated = True
        if self._is_chaos and not self._is_chaos_decorated:
            self._is_chaos_decorated = True
            self.decorate()
            self.start_time = time.monotonic()
        if self._is_chaos_decorated and (time.monotonic() - self.start_time >= self.CHAOS_PERF_TIME):
            self._is_restart = True
            self.decorate()
        if self._is_restart and (time.monotonic() - self.start_time >= self.CHAOS_PERF_TIME + self.RESTART_TIME):
            self.restart_OSC()

    def reset_timers(self):
        self.txt_blocks['timer_chaos'].set_text(self.timers_default)
        self.txt_blocks['timer_sync'].set_text(self.timers_default)

    def update_txt_blocks(self):
        self.handle_fps(self.txt_blocks['fps'])
        tmr = 'timer_chaos' if self._is_chaos_decorated else 'timer_sync'
        self.handle_timer(self.txt_blocks[tmr], self.start_time)
        if self._is_restart:
            self.reset_timers()

    def decorate(self):
        style_name = 'synced' if not self._is_chaos else 'chaotic'
        style_name = 'restart' if self._is_restart else style_name
        style = self.decoration.get(style_name, {})
    
        self.txt_blocks['status'].set_text(style_name.upper())

        color1 = style.get('color1', 'gray')
        color2 = style.get('color2', 'gray')

        self.line1.set_color(color1)
        self.line2.set_color(color2)
        self.legend.get_lines()[0].set_color(color1)
        self.legend.get_lines()[1].set_color(color2)

        for key, block in self.txt_blocks.items():
            blck_p = self.text_block_prop.get(key, {})
            block.set_color(blck_p.get((style_name), 'gray'))

    def set_x_limits(self):     # rules for x-axis scrolling
        lim_x_left = max(0, self._frame - self.SCROLL_TIME)
        lim_x_right = min(self._frame + self.SCROLL_TIME, self._frame + self.SCROLL_TIME / 5)
        return self.ax.set_xlim(lim_x_left, lim_x_right)

    def trim_data(self):
        if len(self.data) > self.SCROLL_TIME:
            self.data = self.data[1:self.SCROLL_TIME + 1] # faster

    def check_chaos(self, v1, v2):
        if not self._is_chaos and abs(v1 - v2) > self.THRESHOLD:
            self._is_chaos = True

    def get_adc_vals(self):
        # return self.ADC.get_vals()
        val1 = np.random.uniform(0, 2.5)
        if self._frame > 55:
            val2 = np.random.uniform(0, 2.5)
        else:
            val2 = val1 - 0.15
        self.check_chaos(val1, val2)
        return val1, val2

    def clear_data(self):
        self.line1.set_data([], [])
        self.line2.set_data([], [])

    def update_data(self):
        upd_vals = np.array([[self._frame, *self.get_adc_vals()]])
        self.data = np.append(self.data, upd_vals, axis=0)
        self.trim_data()
        self.update_txt_blocks()
        return self.data[:, 0], self.data[:, 1], self.data[:, 2]

    def update_frame(self, frame):
        self._frame = frame
        x, y1, y2 = self.update_data()

        self.line1.set_data(x, y1)
        self.line2.set_data(x, y2)

        self.set_x_limits()
        self.chaos_enabler() # check if chaos started - enable decoration var
        return self.line1, self.line2

    def osc_init(self):
        self._frame = None
        self._is_chaos = False
        self._is_chaos_decorated = False
        self._is_restart = False
        self.data = np.empty((0, 3)) # np array to collect data x, y1, y2
        self.start_time = time.monotonic()
        self.START_TIME = time.monotonic()
        self.decorate()
        self.handle_perfdata(self.txt_blocks['perf_data'])

    def start_OSC(self):
        self.animation = animation.FuncAnimation(self.fig, self.update_frame,
                                                 init_func=self.osc_init,
                                                 interval=self.INTERVAL, 
                                                 save_count=0, 
                                                 blit=False)

    def restart_OSC(self):
        self.animation.event_source.stop()
        time.sleep(1)
        self.clear_data()
        self.start_OSC()

    def show_OSC(self):
        plt.show()

    def handle_perfdata(self, obj):
        txt = f'backend:\n{self.BACK}'
        return obj.set_text(txt)

    def handle_fps(self, obj):
        current_time = time.monotonic()
        elapsed_time = current_time - self.START_TIME
        fps = self._frame / elapsed_time
        txt = f'FPS: {fps:.2f}\nFrame:{self._frame}'
        return obj.set_text(txt)

    @staticmethod
    def handle_timer(obj, start_time):
        elapsed_time = time.monotonic() - start_time
        minu = int(elapsed_time / 60)
        seco = int(elapsed_time % 60)
        mils = int((elapsed_time - int(elapsed_time)) * 1000)
        txt = '{:02d}:{:02d}:{:03d}'.format(minu, seco, mils)
        return obj.set_text(txt)