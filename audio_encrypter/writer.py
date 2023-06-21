from scipy.io.wavfile import write
from shared import datadir, bin_to_dec


def write_wav(rate, data, fname):
    write(datadir.joinpath(fname), rate, data)


def binary_to_wav(rate, bdata, outfile):
    dec_data = bin_to_dec(bdata)
    write_wav(rate, dec_data, outfile)
    return rate, dec_data
