import numpy as np
import pandas as pd
from reader import read_wav


def __get_time_array(sample_rate, dlen):
    return np.arange(0, dlen/sample_rate, 1/sample_rate)


def __get_axis_data(fname):
    rate, data = read_wav(fname)
    return pd.DataFrame({
        'Time[s]': __get_time_array(rate, len(data)),
        fname: data}
    ).set_index("Time[s]", drop=True)


def __get_file_df(*files):
    for file in files:
        yield __get_axis_data(file)


def plot_wav(*files, figsize=(15, 10)):
    return get_file_amps(*files).plot(subplots=True, ylabel="Amplitude", figsize=figsize)


def get_file_amps(*files):
    return pd.concat(list(__get_file_df(*files)), axis=1)






