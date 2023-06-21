from pathlib import Path
import matplotlib.pyplot as plt
from verify import plot_wav

datadir = Path('../data')
wavedir = datadir.joinpath('wav48')


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    return wavedir.joinpath(f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ax = plot_wav(get_speaker_file(340, 340), datadir.joinpath("out/test.wav"))
    plt.show()
