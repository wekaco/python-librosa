import librosa
import soundfile as sf
import numpy as np

def convert(file_path, name):
    y, sr = librosa.load(f'{file_path}/{name}')

    # Get the magnitude spectrogram
    S = np.abs(librosa.stft(y))

    # Invert using Griffin-Lim
    y_inv = librosa.griffinlim(S)

    min_length = min([ len(i) for i in [ y, y_inv ] ])

    left_channel = y[0:min_length].reshape(min_length, 1)
    right_channel = y_inv[0:min_length].reshape(min_length, 1)

    sf.write(f'{file_path}/stereo_{name}.wav', np.hstack((left_channel, right_channel)), sr)


def convert_cqt(file_path, name):
    y, sr = librosa.load(f'{file_path}/{name}')

    # Get the CQT magnitude, 7 octaves at 36 bins per octave
    C = np.abs(librosa.cqt(y=y, sr=sr, bins_per_octave=36, n_bins=7*36))

    # Invert using Griffin-Lim
    y_inv = librosa.griffinlim_cqt(C, sr=sr, bins_per_octave=36)

    # And invert without estimating phase
    y_icqt = librosa.icqt(C, sr=sr, bins_per_octave=36)

    min_length = min([ len(i) for i in [ y, y_inv ] ])

    left_channel = y_icqt[0:min_length].reshape(min_length, 1)
    right_channel = y_inv[0:min_length].reshape(min_length, 1)

    sf.write(f'{file_path}/stereo_cqt_{name}.wav', np.hstack((left_channel, right_channel)), sr)

file_path = 'data/916a97d9-dca1-46d9-bf4b-d08958fd0883'
for i in np.arange(10):
    name = f'audio1-{i}.wav'
    print(f'convert > {name}')
    convert(file_path, name)
    print(f'convert cqt > {name}')
    convert_cqt(file_path, name)


