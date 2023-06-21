from scipy.io.wavfile import read
import io
from conversion import dec_to_bin


def wav_to_binary(fname):
    rate, data = read(io.BytesIO(fname.open('rb').read()))
    return rate, dec_to_bin(data)

