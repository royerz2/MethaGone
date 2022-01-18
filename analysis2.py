import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.ticker as mticker
from tqdm import tqdm
import pendulum


df1 = pd.read_csv("sensor1.csv")
df2 = pd.read_csv("sensor2.csv")

plt.style.use("seaborn")
myLocator = mticker.MultipleLocator(50)


class Data:
    def __init__(self, dataFrame, rolling_avg):
        self.rolling_avg = rolling_avg
        self.dataFrame = dataFrame

        self.filled_df = time_filler(self.dataFrame)
        self.smoothened_df = x_moving_average(self.filled_df, 7)

        request_plot(self.smoothened_df)


def x_moving_average(raw_array, x):

    if (x % 2) == 0:
        print("{0} is Even number".format(x))
        print("Rolling average value should be an odd number.")
        raise EOFError

    averaged_array = np.array([])

    span = int(x/2-0.5)

    tbai = raw_array[:span]
    print(tbai)
    tbaf = raw_array[len(raw_array) - span:]
    print(tbaf)
    averaged_array = np.append(averaged_array, tbai)

    for i in range(span, len(raw_array) - span):
        sumlist = []
        print(i)
        for k in range(i - span, i + span +1):
            if raw_array[k] != "n/a":
                sumlist.append(raw_array[k])
            print(k)
            print(sumlist)
        tba = sum(sumlist)/x
        print(tba)

        averaged_array = np.append(averaged_array, tba)

        print(averaged_array)

    averaged_array = np.append(averaged_array, tbaf)

    return averaged_array


def request_plot(dataframe, title):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)

    fig.suptitle(title)
    ax1.plot_date(dataframe["time"], x_moving_average(dataframe["methane"], 5),
                  linestyle="solid", markersize=0, label="Methane")

    ax2.plot_date(dataframe["time"], x_moving_average(dataframe["hydrogen"], 5),
                  linestyle="solid", markersize=0, label="Hydrogen")

    ax3.plot_date(dataframe["time"], x_moving_average(dataframe["temperature"], 5),
                  linestyle="solid", markersize=0, label="Temperature")

    ax4.plot_date(dataframe["time"], x_moving_average(dataframe["humidity"], 5),
                  linestyle="solid", markersize=0, label="Humidity")

    ax1.xaxis.set_major_locator(myLocator)
    ax2.xaxis.set_major_locator(myLocator)
    ax3.xaxis.set_major_locator(myLocator)
    ax4.xaxis.set_major_locator(myLocator)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    figure(figsize=(8, 6), dpi=80)
    plt.show()


def time_filler(dataframe):

    filled_time = []

    gaped_time = dataframe["time"]

    max_ = gaped_time.max()
    min_ = gaped_time.min()

    t1 = pendulum.parse(min_)
    t2 = pendulum.parse(max_)

    time_list = min_.split(":")

    delta = t2 - t1

    for i in tqdm(range(delta.seconds)):

        if int(time_list[2]) < 59:

            time_list[2] = str(int(time_list[2]) + 1)

        elif int(time_list[2]) == 59 and int(time_list[1]) < 59:

            time_list[2] = "00"
            time_list[1] = str(int(time_list[1]) + 1)

        elif int(time_list[1]) == 59 and int(time_list[0]) < 23:

            time_list[2] = "00"
            time_list[1] = "00"
            time_list[0] = str(int(time_list[0]) + 1)

        elif int(time_list[0]) == 23:

            time_list[2] = "00"
            time_list[1] = "00"
            time_list[0] = "00"

        else:
            raise Warning

        added_time = time_list[0].zfill(2) + ":" + time_list[1].zfill(2) + ":" + time_list[2].zfill(2)
        df_line = pd.DataFrame.from_dict({"methane": ["n/a"],
                                          "hydrogen": ["n/a"],
                                          "humidity": ["n/a"],
                                          "temperature": ["n/a"],
                                          "time": [added_time]})

        if str(df_line.time[0]) not in gaped_time.values.tolist():
            dataframe = pd.concat([df_line, dataframe])

    dataframe["time"] = pd.to_datetime(dataframe.time, format="%H:%M:%S")
    sorted_data_frame = dataframe.sort_values(by=['time'], ignore_index=True)

    print(sorted_data_frame)

    return sorted_data_frame


request_plot(df1, "Sensor 1")
request_plot(df2, "Sensor 2")
