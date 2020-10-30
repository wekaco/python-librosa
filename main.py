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
def load(sr, *targets):
    try:
        print("Loader booted")
        while True:
            file_path = (yield)
            print(f'Loading {file_path}', sr)
            y, _ = librosa.load(file_path, sr=sr)
            for t in targets:
                print(t)
                t.send(y)
    except GeneratorExit:
        print("Loader shutdown")
        for t in targets:
            t.close()

@coroutine
def spectogram(*targets):
    try:
        print("Spectogram booted")
        while True:
            y = (yield)
            # Get the magnitude spectrogram
            S = np.abs(librosa.stft(y))
            for t in targets:
                print(t)
                t.send(S)
    except GeneratorExit:
        print("Spectogram shutdown")
        for t in targets:
            t.close()


@coroutine
def griffinlim(*targets):
    try:
        print("Griffinlim booted")
        while True:
            S = (yield)
            # Invert using Griffin-Lim
            y_inv = librosa.griffinlim(S)
            for t in targets:
                print(t)
                t.send(y_inv)
    except GeneratorExit:
        print("Griffinlim shutdown")
        for t in targets:
            t.close()


@coroutine
def merger(channels=2, *targets):
    try:
        print("Merger booted")
        while True:
            _data = []
            for i in range(channels):
                y = (yield)
                print(f'- channel {i}')
                _data.append(y)
            
            def _crop(c, length):
                return c[0:length]

            min_length = min([ len(i) for i in _data ])

            y_merged = np.hstack(
                tuple([ _crop(c, min_length).reshape(min_length, 1) for c in _data ])
            )
            for t in targets:
                print(t)
                t.send(y_merged)
    except GeneratorExit:
        print("Merger shutdown")
        for t in targets:
            t.close()


@coroutine
def write(file_path, sr):
    try:
        print("Writer booted")
        i = 0
        while True:
            y = (yield)
            sf.write('{}_{}.wav'.format(file_path, i),  y, sr)
            i = i + 1
    except GeneratorExit:
        print("Writer shutdown")

import argparse
from os import walk, path
import uuid

class Op:
    GRIFFINLIM = 'griffinlim'

def main(id: uuid.UUID, sample_rate: int, op: Op):
    assert Op.GRIFFINLIM == op

    in_path = path.join('data', id)
    out_path = path.join('data', id, '{}_output'.format(op))

    output_merger = merger(2, write(out_path, sample_rate))
    loader = load(sample_rate,
        spectogram(
            griffinlim(output_merger)
        ),
        output_merger
    )
    
    for (_, _d, sources) in walk(in_path):
        for src in sources:
            loader.send(path.abspath(path.join(in_path, src)))
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
