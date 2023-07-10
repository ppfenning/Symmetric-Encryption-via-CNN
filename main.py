from pathlib import Path
from os import getenv
from dotenv import load_dotenv
from audio_encrypter.chaotic_audio_encryption import chaotic_audio_encryption
from audio_encrypter.verify import compare_files

config = Path("../config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
KEYPATH = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/private_key.pkl")))
OUTDIR = Path(getenv('OUTDIR', default=DATADIR.joinpath("out")))


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    return DATADIR.joinpath('wav48', f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    in_file = get_speaker_file(340, 340)
    encrypt_file = OUTDIR.joinpath('encrypted.wav')
    decrypt_file =  OUTDIR.joinpath('decrypted.wav')

    encrypt = chaotic_audio_encryption(in_file, encrypt_file, KEYPATH)
    decrypt = chaotic_audio_encryption(encrypt_file, decrypt_file, KEYPATH)
    comp = compare_files(in_file, decrypt_file)
