from enum import Enum

import librosa
import soundfile as sf
import numpy as np

from natsort import natsorted

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
def stft(*targets):
    try:
        print("stft booted")
        while True:
            y = (yield)
            # Get the magnitude spectrogram
            S = np.abs(librosa.stft(y))
            for t in targets:
                print(t)
                t.send(S)
    except GeneratorExit:
        print("stft shutdown")
        for t in targets:
            t.close()


@coroutine
def cqt(sample_rate, *targets):
    try:
        print("cqt booted")
        while True:
            y = (yield)
            C = np.abs(librosa.cqt(y, sr=sample_rate, bins_per_octave=36, n_bins=7*36))
            for t in targets:
                print(t)
                t.send(C)
    except GeneratorExit:
        print("stft shutdown")
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
def griffinlim_cqt(*targets):
    try:
        print("Griffinlim cqt booted")
        while True:
            C = (yield)
            # Invert using Griffin-Lim
            y_inv = librosa.griffinlim_cqt(C, bins_per_octave=36)
            for t in targets:
                print(t)
                t.send(y_inv)
    except GeneratorExit:
        print("Griffinlim sqt shutdown")
        for t in targets:
            t.close()


@coroutine
def channel_merger(channels=2, *targets):
    try:
        print("Channel Merger booted")
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
        print("Channel Merger shutdown")
        for t in targets:
            t.close()


@coroutine
def write(file_path, sr):
    try:
        print("Writer booted")
        while True:
            y = (yield)
            sf.write(file_path, y, sr)
    except GeneratorExit:
        print("Writer shutdown")


@coroutine
def harmonic(margin, *targets):
    try:
        print(f"Harmonic booted: margin={margin}")
        while True:
            y = (yield)
            # Invert using Griffin-Lim
            y_harm = librosa.effects.harmonic(y, margin=margin)
            for t in targets:
                print(t)
                t.send(y_harm)
    except GeneratorExit:
        print("Harmonic shutdown")
        for t in targets:
            t.close()


@coroutine
def percussive(margin, *targets):
    try:
        print(f"Percussive booted: margin={margin}")
        while True:
            y = (yield)
            # Invert using Griffin-Lim
            y_perc = librosa.effects.percussive(y, margin=margin)
            for t in targets:
                print(t)
                t.send(y_perc)
    except GeneratorExit:
        print("Percussive shutdown")
        for t in targets:
            t.close()


@coroutine
def add(*targets):
    try:
        print(f"Add booted")
        while True:
            y = (yield)
            x = (yield)
            # Invert using Griffin-Lim
            y_add = y+x
            for t in targets:
                print(t)
                t.send(y_add)
    except GeneratorExit:
        print("Add shutdown")
        for t in targets:
            t.close()


@coroutine
def subtract(*targets):
    try:
        print(f"Subtract booted")
        while True:
            y = (yield)
            x = (yield)
            # Invert using Griffin-Lim
            y_sub = y-x
            for t in targets:
                print(t)
                t.send(y_sub)
    except GeneratorExit:
        print("Subtract shutdown")
        for t in targets:
            t.close()


import argparse
from os import walk, path
import uuid

class Op(Enum):
    GRIFFINLIM = 'griffinlim'
    GRIFFINLIM_CQT = 'griffinlim_cqt'
    HPSS = 'hpss'


def main(id: uuid.UUID, sample_rate: int, op: Op):
    op = Op(op)

    def _griffinlim(abspath, filename, sample_rate):
        out_path = path.join(abspath, f'griffinlim_{filename}')
        _out = write(out_path, sample_rate)
        _stereo = channel_merger(2, _out)

        return [
            stft(
                griffinlim(_stereo)
            ),
            _stereo
        ]

    def _griffinlim_cqt(abspath, filename, sample_rate):
        out_path = path.join(abspath, f'griffinlim_cqt_{filename}')
        _out = write(out_path, sample_rate)
        _stereo = channel_merger(2, _out)

        return [
            cqt(sample_rate,
                griffinlim_cqt(_stereo)
            ),
            _stereo
        ]

    def _hpss(abspath, filename, sample_rate):
        _targets = []
        h_margin = 1
        p_margin = 2

        out_path = path.join(abspath, f'residual_h{h_margin}_p{p_margin}_{filename}')
        _residual = subtract(write(out_path, sample_rate))
        _targets.append(_residual)

        _add = add(_residual)
        out_path = path.join(abspath, f'harm{h_margin}_{filename}')
        _out_harmonic = harmonic(h_margin,
            _add,
            write(out_path, sample_rate)
        )
        _targets.append(_out_harmonic)

        out_path = path.join(abspath, f'perc{p_margin}_{filename}')
        _out_perc = percussive(p_margin,
            _add,
            write(out_path, sample_rate)
        )
        _targets.append(_out_perc)
        return _targets

    in_path = path.join('data', id)
    for (_, _d, sources) in walk(in_path):
        for src in natsorted(sources):
            _targets = []
            if op == Op.GRIFFINLIM:
                _targets = _griffinlim(in_path, src, sample_rate)
            if op == Op.GRIFFINLIM_CQT:
                _targets = _griffinlim_cqt(in_path, src, sample_rate)
            if op == Op.HPSS:
                _targets = _hpss(in_path, src, sample_rate)

            _chain = load(sample_rate, *_targets)
            _chain.send(path.abspath(path.join(in_path, src)))
            _chain.close()

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
        help='|'.join([ op.value for op in Op])
    )
    #parser.set_defaults(**default_params)

    main(**vars(parser.parse_args()))
