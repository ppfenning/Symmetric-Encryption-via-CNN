from pathlib import Path
from os import getenv

import pandas as pd
import numpy as np
from dotenv import load_dotenv
from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption
from audio_encrypter.verify import compare_files, run_folder_stats, get_file_amps, PSNR, wav_entropy

config = Path("../config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
PLAIN_FILES = DATADIR.joinpath("check_1")
ENCRYPTED_FILES = DATADIR.joinpath("encrypt_1")
DECRYPTED_FILES = DATADIR.joinpath("decrypt_1")
KEYPATH_1 = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key/")))

DATADIR.mkdir(exist_ok=True)
PLAIN_FILES.mkdir(exist_ok=True)
ENCRYPTED_FILES.mkdir(exist_ok=True)
DECRYPTED_FILES.mkdir(exist_ok=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    run_folder_stats(PLAIN_FILES, ENCRYPTED_FILES, "", KEYPATH_1, 1)
    run_folder_stats(ENCRYPTED_FILES, DECRYPTED_FILES, "", KEYPATH_1, 1)

    p_files = list(PLAIN_FILES.iterdir())
    p_files.sort()

    enc_files = list(ENCRYPTED_FILES.iterdir())
    enc_files.sort()

    dec_files = list(DECRYPTED_FILES.iterdir())
    dec_files.sort()

    p1_enc = np.zeros((2, 2))
    p1_dec = np.zeros((2, 2))
    enc_dec = np.zeros((2, 2))

    dec_psnr = 0
    enc_psnr = 0
    random_psnr = 0

    entropy_diff = 0

    ch_cnt = 0

    for p_file, enc_file, dec_file in zip(p_files, enc_files, dec_files):

        enc, dec, p1 = get_file_amps(enc_file,  dec_file, p_file)

        enc_psnr += PSNR(p1.to_numpy(), enc.to_numpy())
        random_psnr += PSNR(p1.to_numpy(), np.random.random(p1.shape))
        dec_psnr += PSNR(p1.to_numpy(), dec.to_numpy())

        for i in range(p1.shape[1]):

            p1_enc += np.corrcoef(p1.iloc[:, i], enc.iloc[:, i])
            p1_dec += np.corrcoef(p1.iloc[:, i], dec.iloc[:, i])
            enc_dec += np.corrcoef(enc.iloc[:, i], dec.iloc[:, i])

            entropy_diff += wav_entropy(enc.iloc[:, i]) - wav_entropy(p1.iloc[:, i])

            ch_cnt += 1

    p1_enc = p1_enc/ch_cnt
    p1_dec = p1_dec/ch_cnt
    enc_dec = enc_dec/ch_cnt

    dec_psnr = dec_psnr/len(p_files)
    enc_psnr = enc_psnr/len(p_files)
    random_psnr = random_psnr/len(p_files)

    entropy_diff = entropy_diff/len(p_files)
