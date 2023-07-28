from pathlib import Path
from os import getenv
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption, read_wav, write_wav, chaotic_ciphertext
from audio_encrypter.verify import compare_files

config = Path("config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
KEYPATH = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/private_key.pkl")))
OUTDIR = Path(getenv('OUTDIR', default=DATADIR.joinpath("out")))


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    """
    The get_speaker_file function takes a speaker_id and section_no as arguments,
    and returns the path to the corresponding audio file.

    :param speaker_id: int: Specify the speaker id
    :param section_no: int: Specify the section number of the audio file
    :return: The path to the wav file of a given speaker and section
    :doc-author: Trelent
    """
    return DATADIR.joinpath('wav48', f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


def get_speaker_full(speaker_id: int) -> Path:
    """
    The get_speaker_full function takes a speaker id and returns the full audio file for that speaker.
    It does this by first checking if the output file already exists, and if it doesn't, then it creates
    the output file by concatenating all of the wav files in that speakers folder. It then returns
    the path to this new or existing audio file.

    :param speaker_id: int: Specify the speaker id
    :return: The path to the wav file for a given speaker
    :doc-author: Trelent
    """
    speaker = DATADIR.joinpath('wav48', f"p{speaker_id}")
    outfile = OUTDIR.joinpath(f"{speaker.name}.wav")
    if not outfile.exists():
        folder = list(speaker.rglob('*.wav'))
        df = pd.DataFrame(list(map(read_wav, folder)), index=folder)
        write_wav(df[0][0], np.concatenate(df.sort_index()[1]), outfile)
    return outfile


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    in_file = get_speaker_full(340)
    encrypt_file = OUTDIR.joinpath('encrypted.wav')
    decrypt_file = OUTDIR.joinpath('decrypted.wav')
    encrypt = chaotic_audio_encryption(in_file, encrypt_file, KEYPATH)
    decrypt = chaotic_audio_encryption(encrypt_file, decrypt_file, KEYPATH)
    comp = compare_files(in_file, decrypt_file)
