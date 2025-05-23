import sounddevice as sd
import numpy as np

class AudioInput:
    def __init__(self, samplerate=44100, device_id=(1, None), channels=2, monitor=False):
        self.samplerate = samplerate
        self.device_id = device_id
        self.channels = channels
        self.data = None
        self.monitor = monitor
        self.num_bars = 30
        self.spectrum_data = None

    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)
        if not isinstance(self.data, np.ndarray):
            self.data = np.zeros_like(outdata)
        if self.monitor:
            outdata[:] = indata
        self.data[:] = indata
    
    def stream_audio(self):
        with sd.Stream(device=(1, None),channels=2, callback=self.callback, blocksize=1024) as stream:
            stream.start()
            while True: pass
            


