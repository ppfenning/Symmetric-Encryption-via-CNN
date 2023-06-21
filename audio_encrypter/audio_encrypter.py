from pathlib import Path
from os import getenv
from verify import compare_files
from dotenv import load_dotenv

env_file = Path("../config/.env")

if env_file.exists():
    load_dotenv(env_file)

datadir = Path(getenv('DATADIR', default="../data"))
wavedir = datadir.joinpath('wav48')
outdir = Path(getenv('OUTDIR', default=datadir.joinpath("out")))


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    return wavedir.joinpath(f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_sum = compare_files(get_speaker_file(340, 340), outdir.joinpath('test.wav'))

