# Adapted from Steve Cox code
from array import array

# Sound detection module

import pyaudio
import wave
import time
import threading
import webrtcvad
import sys
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class SoundDetection:

    def __init__(self, data_handler):

        # File to save the recorded audio
        self.data_handler = data_handler
        self.filename = "Voice_record.wav"
        self.vad_excel = "Voice_activity.csv"

        # Sample format config
        self.FORMAT = pyaudio.paInt16
        # Channels config
        self.channels = 1
        # Sampling frequency configuration
        self.freq = 16000

        # Chunk duration in ms
        self.chunk_duration_ms = 20
        # Chunk to read
        self.chunk_size = int(self.freq * self.chunk_duration_ms / 1000)
        # Chunk bytes
        self.chunk_bytes = self.chunk_size * 2
        # Padding configuration in ms
        self.padding_duration_ms = 1500  # 1 sec judgment
        self.num_padding_chunks = int(self.padding_duration_ms / self.chunk_duration_ms)

        # Window chunks
        self.num_window_chunks = int(240 / self.chunk_duration_ms)
        self.num_window_chunks_end = self.num_window_chunks * 2
        self.start_offset = int(self.num_window_chunks * self.chunk_duration_ms * 0.5 * self.freq)

        # VAD Config
        self.vad = webrtcvad.Vad(3)

        # Raw data variable
        self.data = []
        # Voice activity variable
        self.voice_activity = []

        # Duration config
        self.duration = 5
        self.phrase = 'None'

        # PyAudio object initialization
        self.p = pyaudio.PyAudio()
        self.streaming_object()

        # Data
        self.last_value = False
        self.change = 0
        self.voice_act = 0
        self.voice_deac = 0

    def streaming_object(self):
        # Function to set the voice recorder and open the input channel
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.channels,
                                  rate=self.freq,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk_size)
        self.frames = []
        self.frames_duration = 10  # ms

    def normalize(self, snd):
        self.maximum = 32767
        self.times = float(self.maximum) / max(abs(i) for i in snd)
        self.r = array('h')
        for i in snd:
            self.r.append(int(i * self.times))
        return self.r

    def start(self):
        self.go_on = True

    def process(self):
        while self.go_on:
            self.got_a_sentence = False
            self.phrase = None
            ring_buffer = collections.deque(maxlen=self.num_padding_chunks)
            triggered = False
            self.voiced_frames = []
            ring_buffer_flags = [0] * self.num_window_chunks
            ring_buffer_index = 0
            ring_buffer_flags_end = [0] * self.num_window_chunks_end
            ring_buffer_index_end = 0
            buffer_in = ''
            self.raw_data = array('h')
            index = 0
            start_point = 0
            start_time = time.time()
            print("* recording: ")
            self.stream.start_stream()

            while not self.got_a_sentence:
                self.chunk = self.stream.read(self.chunk_size)
                self.data.append(self.chunk)
                self.raw_data.extend(array('h', self.chunk))
                index += self.chunk_size
                time_use = time.time() - start_time

                self.active = self.vad.is_speech(self.chunk, self.freq)
                self.voice_activity.append(1 if self.active else 0)

                ring_buffer_flags[ring_buffer_index] = 1 if self.active else 0
                ring_buffer_index += 1
                ring_buffer_index %= self.num_window_chunks

                ring_buffer_flags_end[ring_buffer_index_end] = 1 if self.active else 0
                ring_buffer_index_end += 1
                ring_buffer_index_end %= self.num_window_chunks_end

                # Start point detection
                if not triggered:
                    ring_buffer.append(self.chunk)
                    self.num_voiced = sum(ring_buffer_flags)
                    if self.num_voiced > 0.8 * self.num_window_chunks:
                        self.phrase = 'Open'
                        triggered = True
                        start_point = index - self.chunk_size * 20
                        ring_buffer.clear()
                # End point detection
                else:
                    ring_buffer.append(self.chunk)
                    self.num_unvoiced = self.num_window_chunks_end - sum(ring_buffer_flags_end)
                    if self.num_unvoiced > 0.90 * self.num_window_chunks_end or time_use > 8:
                        print('Outside triggered')
                        self.phrase = 'Close'
                        triggered = False
                        self.got_a_sentence = True
                sys.stdout.flush()
        sys.stdout.write('\n')

    def test(self, m):
        new_value = m
        if new_value is not None and new_value != self.last_value:
            if new_value:
                self.change = 1
                self.voice_act += 1
            else:
                self.change = 2
                time.sleep(3)
                self.voice_deac += 1
        else:
            self.change = 0
        self.last_value = new_value
        return [self.change, self.voice_act, self.voice_deac]

    def pause(self):
        self.go_on = False

    def close(self):
        print("Finished recording.")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def write_audio(self, path):
        self.wf = wave.open(os.path.join(path, self.filename), "wb")
        self.wf.setnchannels(self.channels)
        self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        self.wf.setframerate(self.freq)
        self.wf.writeframes(b"".join(self.data))
        self.wf.close()

        self.voice_acd = np.array(self.voice_activity)
        pd.DataFrame(self.voice_acd).to_csv(os.path.join(path, self.vad_excel))

    def getData(self):
        [change, voice_act, voice_deac] = self.test(self.active)
        return [self.active, self.change]

    def get_voice(self):
        return self.chunk

    def launch_thread(self):
        self.t = threading.Thread(target=self.process)
        self.t.start()


# def main():
#     sound = SoundDetection(data_handler=None)
#     sound.start()
#     sound.launch_thread()
#     time.sleep(2)
#     for x in range(500):
#         voice = sound.get_voice()
#         data = sound.getData()
#         plt.scatter(x, data[0])
#         plt.pause(0.01)
#         time.sleep(0.01)
#     plt.show
#     sound.pause()
#     sound.close()
#     sound.write_audio(
#         path='C:/Users/Nathalia Cespedes/Desktop/Reminiscence_Interface_Robot/Interface_Plugins/Lower_layer/Speech_Understanding')


# main()
