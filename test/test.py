from pathlib import Path
from os import getenv

import pandas as pd
import numpy as np
from dotenv import load_dotenv
from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption
from audio_encrypter.verify import compare_files, run_folder_stats, get_file_amps, PSNR

config = Path("../config/.env")

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

    run_folder_stats(PLAIN_FILES, ENCRYPTED_FILES_2, "", 1, KEYPATH_2)
    run_folder_stats(ENCRYPTED_FILES_2, ENCRYPTED_FILES_1, "", 2, KEYPATH_2)

    p_files = list(PLAIN_FILES.iterdir())
    p_files.sort()

    k1_files = list(ENCRYPTED_FILES_1.iterdir())
    k1_files.sort()

    k2_files = list(ENCRYPTED_FILES_2.iterdir())
    k2_files.sort()

    p1_k1 = np.zeros((2, 2))
    p1_k2 = np.zeros((2, 2))
    k1_k2 = np.zeros((2, 2))

    k2_psnr = 0
    k1_psnr = 0
    inter_psnr = 0

    ch_cnt = 0

    for p_file, k1_file, k2_file in zip(p_files, k1_files, k2_files):
        k1, k2, p1 = get_file_amps(k1_file,  k2_file, p_file)
        k2_psnr += PSNR(p1.to_numpy(), k2.to_numpy())
        k1_psnr += PSNR(p1.to_numpy(), k1.to_numpy())
        inter_psnr += PSNR(k1.to_numpy(), k2.to_numpy())
        for i in range(p1.shape[1]):
            p1_k1 += np.corrcoef(p1.iloc[:, i], k1.iloc[:, i])
            p1_k2 += np.corrcoef(p1.iloc[:, i], k2.iloc[:, i])
            k1_k2 += np.corrcoef(k1.iloc[:, i], k2.iloc[:, i])
            ch_cnt += 1

    p1_k1 = p1_k1/ch_cnt
    p1_k2 = p1_k2/ch_cnt
    k1_k2 = k1_k2/ch_cnt

    k2_psnr = k2_psnr/len(p_files)
    k1_psnr = k1_psnr/len(p_files)
    inter_psnr = inter_psnr/len(p_files)
