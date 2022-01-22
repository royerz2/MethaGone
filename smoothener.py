import pandas as pd
import numpy as np
from tqdm import tqdm

df1 = pd.read_csv('sensor1.csv')

start_index = 1758  # Set to zero to begin from initial entry.
end_index = len(df1.index)  # Set to len(df1.index) to go to the end.


def spike_hunter(dataframe):
    for i in tqdm(range(start_index, end_index)):

        if (abs(dataframe.methane[i]-dataframe.methane[i+1]) > 100) &\
         (abs(dataframe.methane[i+1]-dataframe.methane[i+2]) > 100):
            dataframe = dataframe.drop(dataframe[i+1])

        if (abs(dataframe.hydrogen[i]-dataframe.hydrogen[i+1]) > 100) &\
         (abs(dataframe.hydrogen[i+1]-dataframe.hydrogen[i+2]) > 100):
            dataframe = dataframe.drop(dataframe[i+1])



def subdrop(dataframe, type):

    dataframe = dataframe.drop(dataframe[
                  (dataframe.methane < 200) |
                  (dataframe.hydrogen < 200) |
                  (dataframe.temperature < 20) |
                  (dataframe.humidity < 20)].index)


def x_moving_average(raw_array, x):

    if (x % 2) == 0:
        print("{0} is Even number".format(x))
        print("Rolling average value should be an odd number.")
        raise EOFError

    averaged_array = np.array([])

    span = int(x / 2 - 0.5)

    tbai = raw_array[:(span + start_index)]
    tbaf = raw_array[len(raw_array) - span:]
    averaged_array = np.append(averaged_array, tbai)

    for i in tqdm(range(start_index + span, len(raw_array) - span)):
        sumlist = []
        for k in range(i - span, i + span + 1):
            continuum = 0
            while continuum == 0:
                try:
                    if raw_array[k] != "n/a":
                        sumlist.append(raw_array[k])
                        continuum = 1
                except KeyError:
                    print('IndexError, getting next value')
                    k += 1

        tba = sum(sumlist) / x

        averaged_array = np.append(averaged_array, tba)

    averaged_array = np.append(averaged_array, tbaf)

    return averaged_array
