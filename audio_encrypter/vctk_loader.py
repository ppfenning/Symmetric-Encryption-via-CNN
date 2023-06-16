import pandas as pd
from functools import reduce
from pathlib import Path
from scipy.io.wavfile import read, write
import io
import numpy as np

datadir = Path('../data')
wavedir = datadir.joinpath('wav48')
id_map = pd.read_csv(datadir.joinpath('speaker-info.txt')).set_index('ID', drop=True).to_dict(orient='index')


def __get_fpath(speaker_id, section_no):
    return wavedir.joinpath(f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


def __read_file(fpath):
    return fpath.open('rb').read()


def __wav_bytes(wdata):
    return io.BytesIO(wdata)


def __read_wav(wbytes):
    return read(wbytes)


def wav_to_binary(speaker_id, section_no):
    rate, data = __read_wav(__wav_bytes(__read_file(__get_fpath(speaker_id, section_no))))
    return rate, pd.Series(data).apply(bin)


def __bin_to_dec(data):
    return data.apply(lambda x: int(x, 2)).to_numpy().astype(np.int16)


def __write_wav(rate, data, fname):
    write(datadir.joinpath(fname), rate, data)


def binary_to_wav(rate, bdata, outfile):
    dec_data = __bin_to_dec(bdata)
    __write_wav(rate, dec_data, outfile)
    return rate, dec_data


if __name__ == '__main__':
    sample_rt, conv_data = binary_to_wav(*wav_to_binary(340, 340), 'test.wav')
