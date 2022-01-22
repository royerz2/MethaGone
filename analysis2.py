import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import pendulum
from matplotlib.pyplot import figure
from tqdm import tqdm

df1 = pd.read_csv("sensor1.csv")  # Assigns sensor data from probe 1 to variable.
df2 = pd.read_csv("sensor2.csv")  # Assigns sensor data from probe 2 to variable.

#################################################### PARAMETERS #######################################################

start_index = 1758  # Set to zero to begin from initial entry.
end_index = 9999  # Set to len(df1.index) to go to the end.
applyThreshold = True  # See the plot with threshold values, then turn to true.
applyAntiAliasing = True  # See the plot before Anti-Aliasing, then turn to true.

plt.style.use("seaborn")  # Sets design language of the plots.
myLocator = mticker.MultipleLocator(100)  # Sets x axis timestamp frequency.


#######################################################################################################################

class Data:  # Defines analysis algorithm for data object. Acts as a meta-function.
    def __init__(self, dataframe, rolling_avg):
        self.data = dataframe.drop(index=df1.index[:start_index],
                                   axis=0)  # Sets min point of data range to be analyzed.

        self.data = self.data.drop(index=df1.index[(end_index + 1):],
                                   axis=0)  # Sets max point of data range to be analyzed.

        self.data = self.data.reset_index(drop=True)  # Reset index to prevent gaps that raise errors during averaging.

        if applyThreshold:
            # Apply thresholds to dataframe for plot readability.
            droplist = self.data[(self.data.methane < 200) |
                                 (self.data.hydrogen < 200) |
                                 (self.data.temperature < 20) |
                                 (self.data.humidity < 20) |
                                 (self.data.methane > 1023) |
                                 (self.data.hydrogen > 1023)].index

            self.data = self.data.drop(droplist)

            self.data = self.data.reset_index(drop=True)

        print('Data description prior to data wrangling')
        df_describe(self.data)

        print(df1)  # Provides overview of the dataframe to be analyzed.

        df_describe(self.data)  # Describes general aspects of the data; Var, Avg, Corr.

        # Applies rolling average method to smoothen the data.
        if applyAntiAliasing:

            self.toPlot = pd.DataFrame({'methane': x_moving_average(self.data.methane, rolling_avg),
                                        'hydrogen': x_moving_average(self.data.hydrogen, rolling_avg),
                                        'time': self.data.time,
                                        'humidity': self.data.humidity,
                                        'temperature': self.data.temperature},
                                       columns=['methane', 'hydrogen', 'time', 'humidity', 'temperature'])

            print(self.toPlot.head(5))

            request_plot(self.toPlot, 'Sensor 1 Data')  # Applies rolling average method to smoothen the data.

        else:
            request_plot(self.data, 'Sensor 1 Data')

        print('Data description after data wrangling')
        df_describe(self.data)


def x_moving_average(raw_array, x):

    if (x % 2) == 0:
        print("{0} is Even number".format(x))
        print("Rolling average value should be an odd number.")
        raise EOFError

    averaged_array = np.array([])

    span = int(x / 2 - 0.5)

    tbai = raw_array[:span]
    tbaf = raw_array[len(raw_array) - span:]

    averaged_array = np.append(averaged_array, tbai)

    for i in tqdm(range(span, len(raw_array) - span)):
        sumlist = []
        for k in range(i - span, i + span + 1):
            if raw_array[k] != "n/a":
                sumlist.append(raw_array[k])
        tba = sum(sumlist) / x

        averaged_array = np.append(averaged_array, tba)

    averaged_array = np.append(averaged_array, tbaf)

    return averaged_array


def anti_aliasing(dataframe):
    for i in tqdm(range(start_index, end_index)):

        if (abs(dataframe.hydrogen[i] - dataframe.hydrogen[i + 1]) > 100) or \
                (abs(dataframe.hydrogen[i + 1] - dataframe.hydrogen[i + 2]) > 100) or \
                (abs(dataframe.methane[i] - dataframe.methane[i + 1]) > 100) or \
                (abs(dataframe.methane[i + 1] - dataframe.methane[i + 2]) > 100):
            dataframe = dataframe.drop(dataframe[i + 1])


def request_plot(dataframe, title):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)

    fig.suptitle(title)
    ax1.plot_date(dataframe["time"], dataframe["methane"],
                  linestyle="solid", markersize=0, label="Methane")

    ax2.plot_date(dataframe["time"], dataframe["hydrogen"],
                  linestyle="solid", markersize=0, label="Hydrogen")

    ax3.plot_date(dataframe["time"], dataframe["temperature"],
                  linestyle="solid", markersize=0, label="Temperature")

    ax4.plot_date(dataframe["time"], dataframe["humidity"],
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


def df_describe(dataframe):
    df = dataframe

    plt.matshow(df.corr())
    plt.title("Correlation Matrix")
    plt.show()

    df.dropna(inplace=True)

    include = ['object', 'float', 'int']

    desc = df.describe(include=include)

    print(desc)


plot = Data(df1, 5)
