from reader import wav_to_binary
from writer import binary_to_wav
from pathlib import Path

datadir = Path('../data')
wavedir = datadir.joinpath('wav48')


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    return wavedir.joinpath(f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rate, x = binary_to_wav(*wav_to_binary(get_speaker_file(340, 340)), outfile=wavedir.joinpath('out/test.wav'))
