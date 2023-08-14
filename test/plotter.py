from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption
from pathlib import Path
from os import getenv

DATADIR = Path(getenv('DATADIR', default="../data"))
PLAIN_FILES = DATADIR.joinpath("check_2")
ENCRYPTED_FILES = DATADIR.joinpath("key_1")
KEYPATH_1 = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key/")))


if __name__ == '__main__':

    fname = "CantinaBand60.wav"
    in_file = PLAIN_FILES.joinpath(fname)
    out_file = ENCRYPTED_FILES.joinpath(fname)
    # Plot the solution
    sol = chaotic_audio_encryption(in_file, out_file, KEYPATH_1)