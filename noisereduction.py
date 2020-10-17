from typing import Optional

from librosa import load
import uuid
import os

import noisereduce as nr
import soundfile as sf

id = '916a97d9-dca1-46d9-bf4b-d08958fd0883'

def _readpath(id: uuid.UUID, n: int):
    return _fullpath(id, n)

def _writepath(id: uuid.UUID, n: int):
    return _fullpath(id, n, 'noisreduction')

def _fullpath(id: uuid.UUID, n: int, prefix: Optional[str] = None):
    name =  f'audio1-{n}.wav'
    if prefix:
        name = '-'.join([ prefix, name ])

    relative_path = os.path.join('data', id, name )
    return os.path.abspath(relative_path)

def main():
    for (i, start, end, (y, samplerate)) in [
        ( 1, 26353, 28110, load(_fullpath(id, 1)) )
    ]:
        noise_clip = y[start:end]
        # perform noise reduction
        reduced_noise = nr.reduce_noise(audio_clip=y, noise_clip=noise_clip, verbose=True)

        sf.write(_writepath(id, i), reduced_noise, samplerate=samplerate)

main()
