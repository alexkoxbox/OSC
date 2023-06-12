
timers_left = 0.08
timers_sync = 0.2
timer_label = 0.05
timers_bottom = 0.20
right_block = 0.90

osc_blocks = {
    'timer_chaos': {
        'padding_left': timers_left,
        'padding_bottom': timers_bottom,
        'fontsize': 18,
        'innertxt': '00:00:000',
        'synced': 'gray',
        'chaotic': 'orangered',
        'restart': 'gray',
    },
    'timer_sync': {
        'padding_left': timers_left,
        'padding_bottom': timers_bottom + timers_sync,
        'fontsize': 18,
        'innertxt': '00:00:00',
        'synced': 'white',
        'chaotic': 'gray',
        'restart': 'gray',
    },
    'timer_lbl_chaos': {
        'innertxt': 'Chaotic',
        'padding_left': timers_left,
        'padding_bottom': timers_bottom + timer_label,
        'synced': 'gray',
        'chaotic': 'orangered',
        'restart': 'gray',
    },
    'timer_lbl_sync': {         # sync
        'innertxt': 'Synced',
        'padding_left': timers_left,
        'padding_bottom': timers_bottom + timer_label + timers_sync,
        'synced': 'white',
        'chaotic': 'gray',
        'restart': 'gray',
    },
    'fps': {
        'innertxt': 'FPS:',
        'padding_left': right_block,
        'padding_bottom': 0.9,
        'horizontalalignment': 'left',
        'synced': 'white',
        'chaotic': 'white',
        'restart': 'gray',
    },
    'perf_data': {
        'innertxt': 'Perf data:',
        'padding_left': right_block,
        'padding_bottom': 0.78,
        'horizontalalignment': 'left',
        'synced': 'gray',
        'chaotic': 'gray',
        'restart': 'gray',
    },
    'status': {
        'innertxt': 'RELOAD',
        'padding_left': right_block,
        'padding_bottom': 0.21,
        'horizontalalignment': 'left',
        'fontsize': 16,
        'synced': 'cyan',
        'chaotic': 'orangered',
        'restart': 'yellow',
    },
}

text_prop = {
    'verticalalignment': 'top',
    'fontfamily': 'monospace'
}

line_decoration = {
    'synced': {
        'color1': 'cyan',
        'color2': 'aquamarine',
        'other': 'cyan'
    },
    'chaotic': {
        'color1': 'orange',
        'color2': 'red',
        'other': 'orange',
    },
    'restart': {
        'color1': 'gray',
        'color2': 'gray',
        'other': 'gray',
    },
}

