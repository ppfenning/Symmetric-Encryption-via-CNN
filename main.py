from pathlib import Path
from os import getenv
import pandas as pd
from dotenv import load_dotenv
from functools import partial
from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption
import matplotlib.pyplot as plt
from audio_encrypter.verify import compare_files, plot_wav
import random
import string

config = Path("config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
PLAIN_FILES = DATADIR.joinpath("plaintext")
ENCRYPTED_FILES = DATADIR.joinpath("encrypted")
DECRYPTED_FILES = DATADIR.joinpath("decrypted")
KEYPATH = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key/")))

DATADIR.mkdir(exist_ok=True)
PLAIN_FILES.mkdir(exist_ok=True)
ENCRYPTED_FILES.mkdir(exist_ok=True)
DECRYPTED_FILES.mkdir(exist_ok=True)


# def aes_encryption(audio_file: Path, encrypted_file):
#     AES_KEY = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))
#     AES_IV = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
#     encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))
#     with audio_file.open(mode="rb") as fd:
#         encrypted_audio = encryptor.encrypt(fd.read())
#     with audio_file.open(mode="wb") as fd:
#         fd.write(encrypted_audio)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stats = dict()
    for in_file in PLAIN_FILES.iterdir():
        encrypt_chaos = ENCRYPTED_FILES.joinpath(f"CHAOS_{in_file.name}")
        size = in_file.lstat().st_size/(1024**2)
        decrypted_chaos = DECRYPTED_FILES.joinpath(f"CHAOS_{in_file.name}")
        nruns = 10
        _, encrypted, avg_time_encrypt = chaotic_audio_encryption(in_file, encrypt_chaos, KEYPATH, nruns)
        stats[in_file.name] = {
            "size": size,
            "encryption_time": avg_time_encrypt,
            "channels": encrypted.ndim
        }
    df = pd.DataFrame(stats).T.sort_values("size")
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(df["size"], df["encryption_time"], c='red', alpha=0.05, edgecolors='none')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.loglog(df["size"], df["encryption_time"])
    plt.show()