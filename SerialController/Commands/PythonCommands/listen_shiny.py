#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button
from Commands.PythonCommandBase import PythonCommand

try:
    import pyaudio
except ImportError:
    print("PyAudio is not installed.")
    pass
except:
    pass

import numpy as np
from datetime import datetime

# import matplotlib.pyplot as plt

'''
I want to detect the sound of a shiny Pokemon.
This script might fulfill that desire.
It reacts when a cry sounds during execution.

You need to input the Switch's sound to the PC in advance.
While using OpenCV (= during video capture), you can't receive the capture board's video by other means,
Moreover, you can't receive sound either (OpenCV doesn't have sound reception function & exclusive processing is done)

For this reason, a bit troublesome procedure is necessary.
Below, I give an example of how to input the Switch's sound to the PC while receiving video.

・Use the capture board's pass-through function to connect the monitor/TV with audio output function (with headphone jack) and Switch, and connect that monitor/TV and PC's microphone jack with male-male AUX cable.

・Since Switch's headphone jack can be used even in TV mode, connect that and PC's microphone jack with male-male AUX cable.
It's easy, but since it's directly connected to Switch, quite a bit of noise is added (depending on the cable)

・Use OBS's VirtualCamera function. OBS has a virtual camera function, and PokeCon can recognize it (lag increases)
(However, it's limited to the plugin version of virtual camera, not the built-in one)
OBS can output the received sound to any device connected to the PC, so connect from that output destination to PC's microphone jack with AUX cable etc.
・Or, you can receive the output by "inputting" from OBS to virtual sound devices like Voicemeeter.
This method doesn't require additional cables, but the settings might be troublesome.
'''


class ListenShiny(PythonCommand):
    NAME = 'Listen to Shiny Sound'

    def __init__(self):
        super().__init__()

    def do(self):

        CHUNK = 1024
        RATE = 44100
        l = 1e7  # 閾値．入力の音量によって変動します．
        sound_count = 0

        data1 = []
        data2 = []

        freqList = np.fft.fftfreq(int(1.5 * RATE / CHUNK) * CHUNK * 2, d=1.0 / RATE)

        p = pyaudio.PyAudio()

        # Uncomment the following to print the device list when the script is executed, so
        # find the device taking in sound and set its index to input_device_index
        # for index in range(0, p.get_device_count()):
        #     print(p. get_device_info_by_index(index))
        device_index = 1

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,  # 1: モノラル
                        input_device_index=device_index,
                        rate=RATE,
                        frames_per_buffer=CHUNK,
                        input=True,
                        output=False)
        self._logger.debug(f"Connect: {p.get_device_info_by_index(device_index)}")
        try:
            while stream.is_active():  # Infinite loop
                if not self.checkIfAlive():
                    # break processing when stop is pressed
                    break
                for i in range(int(1.5 * RATE / CHUNK)):
                    d = np.frombuffer(stream.read(CHUNK), dtype='int16')
                    if sound_count == 0:
                        data1.append(d)

                    else:
                        data1.append(d)
                        data2.append(d)

                if sound_count >= 1:
                    if sound_count % 2 == 1:
                        data = np.asarray(data1).flatten()
                        fft_data = np.fft.fft(data)
                        data1 = []

                    else:
                        data = np.asarray(data2).flatten()
                        fft_data = np.fft.fft(data)
                        data2 = []

                    fft_abs = np.abs(fft_data)  # / (np.max(fft_data)-np.min(fft_data)) * 1e7
                    # I thought about doing something like normalization but didn't understand it well.

                    # plt.plot(freqList, fft_abs)  # For visualization with matplotlib.
                    # # plt.xlim(3400, 4500)
                    # plt.draw() # For graph display
                    # plt.show() # For graph display

                    data3100 = fft_abs[np.where((freqList < 3200) & (freqList > 3000))]  # Frequency components around 3100Hz
                    data4200 = fft_abs[np.where((freqList < 4400) & (freqList > 4150))]  # Frequency components around 4200Hz

                    if (data3100.max() > 0.4 * l) and (data4200.max() > 1 * l):
                        # When the intensity around 3100Hz and 4200Hz is above a certain level, judge as shiny
                        # Since 4200Hz is stronger, multiplied the threshold by 0.4.
                        # Looking at the spectrum, it seems like 3100Hz might be a harmonic, so maybe add recognition for that too.

                        this_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        # If you want to save the sound when encountered, uncomment the following
                        # file_name = this_time + ".wav"
                        #
                        # wf = wave.open(file_name, 'w')
                        # wf.setnchannels(1)
                        # wf.setsampwidth(2)
                        # wf.setframerate(RATE)
                        # wf.writeframes(data)
                        # wf.close()

                        print("Sounds Shiny!" + this_time)
                        self._logger.debug("Recognized sound.")
                        data1 = []
                        data2 = []
                        sound_count = 0

                sound_count += 1

            stream.stop_stream()
            stream.close()
            p.terminate()

        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
