import librosa
import soundfile as sf
import numpy as np

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start

@coroutine
def load(sr):
    try:
        while True:
            file_path = (yield)
            print(f'Loading {file_path}', sr)
            y, _ = librosa.load(file_path, sr=sr)
    except GeneratorExit:
        print("Loaded")


def convert(file_path, name, sr):
    y, _ = librosa.load(f'{file_path}/{name}', sr=sr)

    # Get the magnitude spectrogram
    S = np.abs(librosa.stft(y))

    # Invert using Griffin-Lim
    y_inv = librosa.griffinlim(S)

    min_length = min([ len(i) for i in [ y, y_inv ] ])

    left_channel = y[0:min_length].reshape(min_length, 1)
    right_channel = y_inv[0:min_length].reshape(min_length, 1)

    sf.write(f'{file_path}/stereo_{name}', np.hstack((left_channel, right_channel)), sr)


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

def pre_emphasis(file_path, name):
    import matplotlib.pyplot as plt

    full_path = f'{file_path}/{name}'
    print(f'pre_emphasis: {full_path}')
    y, sr = librosa.load(full_path)

    y_filt = librosa.effects.preemphasis(y, coef=0.5)

    """
    # and plot the results for comparison
    S_orig = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max, top_db=None)
    S_preemph = librosa.amplitude_to_db(np.abs(librosa.stft(y_filt)), ref=np.max, top_db=None)
    fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True)
    librosa.display.specshow(S_orig, y_axis='log', x_axis='time', ax=ax[0])
    ax[0].set(title='Original signal')
    ax[0].label_outer()
    img = librosa.display.specshow(S_preemph, y_axis='log', x_axis='time', ax=ax[1])
    ax[1].set(title='Pre-emphasized signal')
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    """
    write_path = f'pre_emphasis_{name}.wav'
    sf.write(f'{file_path}/{write_path}', y_filt, sr)
    return write_path

"""
for i in np.arange(10):
    name = f'audio1-{i}.wav'
    # pre_emphasis(file_path, name)
    convert(file_path, name)
    # convert_cqt(file_path, name)
"""

import argparse
from os import walk, path
import uuid

class Op:
    GRIFFINLIM = 'griffinlim'

def main(id: uuid.UUID, sample_rate: int, op: Op):
    file_path = path.join('data', id)
    loader = load(sample_rate)
    for (_, _d, sources) in walk(file_path):
        for src in sources:
            loader.send(path.abspath(path.join(file_path, src)))
            """
            path.abspath(path.join(file_path, src)), sample_rate)path.abspath(path.join(file_path, src)), sample_rate)
            if Op.GRIFFINLIM == op:
                convert(file_path, src, sample_rate)
            """
    loader.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        argument_default=argparse.SUPPRESS
    )

    parser.add_argument(
        '--id', required=True,
        help='experiment name'
    )
    parser.add_argument(
        '--sample_rate', type=int, required=True,
        help='sample rate of the file data and generated sound'
    )
    parser.add_argument(
        '--op', type=str, required=True,
        help='|'.join([ Op.GRIFFINLIM ])
    )
    #parser.set_defaults(**default_params)

    main(**vars(parser.parse_args()))
