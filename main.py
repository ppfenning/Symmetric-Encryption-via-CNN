from pathlib import Path
from os import getenv
from dotenv import load_dotenv
from audio_encrypter.audio_encrypter import audio_encrypter
from audio_encrypter.verify import compare_files

config = Path("../config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="data"))
KEYPATH = Path(getenv('KEYPATH', default="~/.chaos-encrypt/private_key.pkl"))
OUTDIR = Path(getenv('OUTDIR', default=DATADIR.joinpath("out")))


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    return DATADIR.joinpath('wav48', f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    _, in_val, encrypt = audio_encrypter(get_speaker_file(340, 340), OUTDIR.joinpath('encrypted.wav'), KEYPATH)
    _, _, decrypt = audio_encrypter(OUTDIR.joinpath('encrypted.wav'), OUTDIR.joinpath('decrypted.wav'), KEYPATH)
    comp = compare_files(get_speaker_file(340, 340), OUTDIR.joinpath('decrypted.wav'))
