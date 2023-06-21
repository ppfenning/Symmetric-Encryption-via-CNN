from scipy.io.wavfile import read
import io
from shared import get_fpath, dec_to_bin


def wav_to_binary(speaker_id, section_no):
    rate, data = read(io.BytesIO(get_fpath(speaker_id, section_no).open('rb').read()))
    return rate, dec_to_bin(data)

