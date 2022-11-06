from scipy.io import wavfile
import matplotlib.pyplot as plt

def read_wav_data(file):
    samplerate, data = wavfile.read(file)
    plt.plot(data)
    plt.show()
    return samplerate, data