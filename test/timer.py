from audio_encrypter.verify import run_folder_stats
from pathlib import Path
from os import getenv

DATADIR = Path(getenv('DATADIR', default="../data"))
PLAIN_FILES = DATADIR.joinpath("plaintext")
ENCRYPTED_FILES = DATADIR.joinpath("encrypted")
KEYPATH_1 = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key/")))


if __name__ == '__main__':
    times = run_folder_stats(PLAIN_FILES, ENCRYPTED_FILES, "", KEYPATH_1, 10)