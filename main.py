# from test_adc import ADC
# from soundsynth import SoundSynth
from osc import OSC

def main():
    # data = ADC()
    # sound = SoundSynth(data)
    # osc = OSC(data)
    osc = OSC(1)
    osc.start_OSC()
    osc.show_OSC() # launch plt.show


if __name__ == '__main__':
    main()