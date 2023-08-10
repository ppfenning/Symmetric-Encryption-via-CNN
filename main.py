from pathlib import Path
from os import getenv

import pandas as pd
import numpy as np
from dotenv import load_dotenv
from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption
from audio_encrypter.verify import compare_files, run_folder_stats, get_file_amps, PSNR

config = Path("config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
PLAIN_FILES = DATADIR.joinpath("check_2")
ENCRYPTED_FILES_2 = DATADIR.joinpath("key_1")
ENCRYPTED_FILES_1 = DATADIR.joinpath("key_2")
DECRYPTED_FILES = DATADIR.joinpath("decrypted")
KEYPATH_1 = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key/")))
KEYPATH_2 = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key_3/")))

DATADIR.mkdir(exist_ok=True)
PLAIN_FILES.mkdir(exist_ok=True)
DECRYPTED_FILES.mkdir(exist_ok=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fname = "CantinaBand60.wav"
    chaotic_audio_encryption(PLAIN_FILES.joinpath(fname), ENCRYPTED_FILES_1.joinpath(fname), KEYPATH_1)
    chaotic_audio_encryption(PLAIN_FILES.joinpath(fname), ENCRYPTED_FILES_2.joinpath(fname), KEYPATH_2)
    comp = compare_files(ENCRYPTED_FILES_1.joinpath(fname), ENCRYPTED_FILES_2.joinpath(fname))
    p1, k1, k2 = get_file_amps(PLAIN_FILES.joinpath(fname),  ENCRYPTED_FILES_1.joinpath(fname), ENCRYPTED_FILES_2.joinpath(fname))
    k2_psnr = PSNR(p1.to_numpy(), k2.to_numpy())
    k1_psnr = PSNR(p1.to_numpy(), k1.to_numpy())
    inter_psnr = PSNR(k1.to_numpy(), k2.to_numpy())
    for i in range(p1.shape[1]):
        print(np.corrcoef(p1.iloc[:, i], k1.iloc[:, i]))
        print(np.corrcoef(p1.iloc[:, i], k2.iloc[:, i]))
        print(np.corrcoef(k1.iloc[:, i], k2.iloc[:, i]))
