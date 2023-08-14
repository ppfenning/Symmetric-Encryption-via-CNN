import pandas as pd
import numpy as np
from audio_encrypter.verify import run_folder_stats
import matplotlib.pyplot as plt
from pathlib import Path
from os import getenv

DATADIR = Path(getenv('DATADIR', default="../data"))
PLAIN_FILES = DATADIR.joinpath("plaintext")
ENCRYPTED_FILES = DATADIR.joinpath("encrypted")
KEYPATH_1 = Path(getenv('KEYPATH', default=Path.home().joinpath(".chaos-encrypt/chaos_key/")))


if __name__ == '__main__':
    #   times = run_folder_stats(PLAIN_FILES, ENCRYPTED_FILES, "", KEYPATH_1, 10)
    times = pd.read_csv("../data/file_times.csv", index_col=0)
    x = times["size"]
    y = times["encryption_time"]
    c = times["channels"]

    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter(x, y, c=c, cmap="Dark2", edgecolors="k", label=c)

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlim(x.min(), x.max()*1.1)
    ax.set_ylim(y.min(), y.max())

    ax.set_xlabel("File Size (MB)")
    ax.set_ylabel("Encryption Times (s)")
    ax.set_title("Log-Log Encryption Time vs File Size")

    legend = ax.legend(*scatter.legend_elements(), loc="upper left", title="Audio Channels")
    ax.add_artist(legend)

    z = np.linspace(x.min()/2, x.max()*1.1)  # start at 1, to avoid error from log(0)

    logA = np.log(x)  # no need for list comprehension since all z values >= 1
    logB = np.log(y)

    m, b = np.polyfit(logA, logB, 1)  # fit log(y) = m*log(x) + c
    y_fit = np.exp(m * np.log(z) + b)  # calculate the fitted values of y

    plt.plot(z, y_fit, ':')

    plt.show()
