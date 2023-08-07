from pathlib import Path
from os import getenv
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from audio_encrypter.chaotic_audio_encryption import (
    chaotic_audio_encryption,
    read_wav,
    write_wav
)
from audio_encrypter.verify import compare_files
from functools import partial
#from Crypto.Cipher import AES
import random
import string
from timeit import timeit

config = Path("config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
PLAIN_FILES = DATADIR.joinpath("plaintext")
ENCRYPTED_FILES = DATADIR.joinpath("encrypted")
DECRYPTED_FILES = DATADIR.joinpath("decrypted")
KEYPATH = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/private_key.pkl")))

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
    fname = "WAV_10MG.wav"
    in_file = PLAIN_FILES.joinpath(fname)
    encrypt_chaos = ENCRYPTED_FILES.joinpath(f"CHAOS_{in_file.name}")
    decrypted_chaos = DECRYPTED_FILES.joinpath(f"CHAOS_{in_file.name}")
    encrypt_aes = ENCRYPTED_FILES.joinpath(f"AES_{in_file.name}")
    *_, t1 = chaotic_audio_encryption(in_file, encrypt_chaos, KEYPATH)
    print(t1)
    *_, t2 = chaotic_audio_encryption(encrypt_chaos, decrypted_chaos, KEYPATH)
    print(t2)
