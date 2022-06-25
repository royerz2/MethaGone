import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.pyplot import figure
from tqdm import tqdm
from datetime import datetime, timedelta

# TODO: Max delta analysis within experimental condition boundaries.

big_df = pd.read_csv("p6_22_06.csv")
df1 = pd.read_csv("p6s1_22_06.csv")
df2 = pd.read_csv("p6s2_22_06.csv")

# /////////////////////////////////////////////////// PARAMETERS ///////////////////////////////////////////////////////

start_index = 0  # Set to zero to begin from initial entry.
end_index = 999999999

bromoformination_index = 2000
bromoformination_time = ''

if bromoformination_index < start_index:
    print("The bromoformination point cannot be earlier than the starting point.")
    raise EOFError

plt.style.use("seaborn")  # Sets design language of the plots.
myLocator = mticker.MultipleLocator(100)  # Sets x axis timestamp frequency.


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Analysis:  # Defines analysis algorithm for data object. Acts as a meta-function.
    def __init__(self, dataframe, applyAntiAliasing, applyThreshold, dataframe2, rolling_avg=5,
                 start=0, end=9999999):

        # self.data = dataframe.drop(index=dataframe.index[:start],
        #                            axis=0)  # Sets min point of data range to be analyzed.
        # print("Deneme:", self.data)
        #
        # self.data = self.data.drop(index=dataframe.index[(end + 1):],
        #                            axis=0)  # Sets max point of data range to be analyzed.

        self.data = dataframe
        self.data = self.data.reset_index(drop=True)  # Reset index to prevent gaps that raise errors during averaging.

        self.threshold = applyThreshold
        if self.threshold:
            self.data = threshold(self.data)

        print('Data description prior to data wrangling')

        # Applies rolling average method to smoothen the data.
        self.antialiasing = applyAntiAliasing
        if self.antialiasing:
            self.toPlot = anti_aliasing(self.data)
            print(self.toPlot.head(5))

            request_plot(self.toPlot, 'Sensor 2 Data')  # Applies rolling average method to smoothen the data.

        else:
            request_plot(self.data, 'Sensor 2 Data')  # Gets plot.

        # normalization factor will be the average difference of the first 12 points and will be applied to df1
        print('Data description after data wrangling')


def x_moving_average(raw_array, x):
    if (x % 2) == 0:  # Check if x is odd for proper functionality.
        print(f"{x} is Even number")
        print("Rolling average value should be an odd number.")
        raise EOFError

    averaged_array = np.array([])

    span = int(x / 2 - 0.5)  # How many data from left and right of a data to average.

    # Unaverageable points set aside to add later
    tbai = raw_array[:span]
    tbaf = raw_array[len(raw_array) - span:]

    averaged_array = np.append(averaged_array, tbai)

    for i in tqdm(range(span, len(raw_array) - span)):
        sumlist = []
        for k in range(i - span, i + span + 1):  # Get points from left and right of i.
            if raw_array[k] != "n/a":
                sumlist.append(raw_array[k])
        tba = sum(sumlist) / x  # Calculate average of points in span around i.

    # Add back the unaverageable points
    averaged_array = np.append(averaged_array, tba)
    averaged_array = np.append(averaged_array, tbaf)

    return averaged_array


def anti_aliasing(dataframe, spike_height=100):
    # Depending on how dynamic the sensor is, define the minimum delta required between calues to eliminate
    for i in tqdm(range(start_index, end_index)):
        # If there are any rows that spike above set spike height up or down, delete it.
        if (abs(dataframe.hydrogen[i] - dataframe.hydrogen[i + 1]) > spike_height) or \
                (abs(dataframe.hydrogen[i + 1] - dataframe.hydrogen[i + 2]) > spike_height) or \
                (abs(dataframe.methane[i] - dataframe.methane[i + 1]) > spike_height) or \
                (abs(dataframe.methane[i + 1] - dataframe.methane[i + 2]) > spike_height):
            dataframe = dataframe.drop(dataframe[i + 1])
    return dataframe


def request_plot(dataframe, title):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)  # Make four subplots.

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

    figure(figsize=(8, 6), dpi=800)
    plt.show()


def comperative_plot(dataframe1, dataframe2):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)  # Make four subplots.

    df = dataframe2.append(dataframe1)
    df.reset_index()
    df.sort_values('time')
    print(df.time)
    df1 = df[(df['sensor'] == 1)]
    df2 = df[(df['sensor'] == 2)]

    # create timeseries between start and end time
    # add values that a. methane doesnt have,
    #                 b. hydrogen doesnt have,
    #                 c. both dont have with n/a's.
    # check with row count after filtering for time.

    start = datetime.datetime.strptime("13:12:50", "%H:%M:%S")
    end = datetime.datetime.strptime("16:56:58", "%H:%M:%S")

    dates_generated = []
    for x in range(0, (end - start).seconds):
        time_to_add = start + datetime.timedelta(seconds=x)
        if time_to_add in df1.time.to_list() and time_to_add not in df2.time.to_list():
            filtered_value1 = df1[(df1['time'] == time_to_add)].iloc[0].methane
            filtered_value2 = df2[(df2['time'] == time_to_add)].iloc[0].methane
            dict = {'methane1': f'{filtered_value1}', 'methane2': f'{filtered_value2}', 'time': f'{time_to_add}'}

            big_df = big_df.append(dict, ignore_index=True)

        elif time_to_add not in df1.time.to_list() and time_to_add in df2.time.to_list():
            filtered_value2 = df2[(df2['time'] == time_to_add)].iloc[0].methane
            dict = {'methane1': 0, 'methane2': f'{filtered_value2}', 'time': f'{time_to_add}'}
            big_df = big_df.append(dict, ignore_index=True)

        elif time_to_add not in df2.time.to_list() and time_to_add in df1.time.to_list():
            filtered_value1 = df1[(df1['time'] == time_to_add)].iloc[0].methane
            dict = {'methane1': f'{filtered_value1}', 'methane2': 0, 'time': f'{time_to_add}'}
            big_df = big_df.append(dict, ignore_index=True)

        else:
            dict = {'methane1': 0, 'methane2': 'n/a', 'time': f'{time_to_add}'}
            big_df = big_df.append(dict, ignore_index=True)
        big_df.to_csv("matched_methane.csv")

    fig.suptitle("Sensor Data Comparison")
    ax1.plot(df1["time"], df1["methane"],
             linestyle="solid", markersize=0, label="Methane")

    ax2.plot(df1["time"], df1["hydrogen"],
             linestyle="solid", markersize=0, label="Hydrogen")

    ax3.plot(df1["time"], df1["temperature"],
             linestyle="solid", markersize=0, label="Temperature")

    ax4.plot(df1["time"], df1["humidity"],
             linestyle="solid", markersize=0, label="Humidity")

    ax1.plot(df2["time"], df2["methane"],
             linestyle="solid", markersize=0, label="Methane")

    ax2.plot(df2["time"], df2["hydrogen"],
             linestyle="solid", markersize=0, label="Hydrogen")

    ax3.plot(df2["time"], df2["temperature"],
             linestyle="solid", markersize=0, label="Temperature")

    ax4.plot(df2["time"], df2["humidity"],
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


def df_describe(dataframe):
    df = dataframe

    # plt.matshow(df.corr())
    # plt.title("Correlation Matrix")
    # plt.show()

    df.dropna(inplace=True)

    include = ['object', 'float', 'int']

    desc = df.describe(include=include)

    print(desc)


def difference_analysis(data1, data2):
    sum1 = 0
    sum2 = 0
    for i in range(1, len(data1) - 1):
        point = data1.iloc[i]
        next_point = data1.iloc[i + 1]

        time1 = datetime.strptime(point.time, "%H:%M:%S")
        time2 = datetime.strptime(next_point.time, "%H:%M:%S")

        time1 = timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
        time2 = timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second)

        delta = datetime.strptime(str(time2 - time1), "%H:%M:%S")
        delta = delta.second

        sum1 += delta * point.methane

    for i in range(1, len(data2) - 1):
        point = data2.iloc[i]
        next_point = data2.iloc[i + 1]

        time1 = datetime.strptime(point.time, "%H:%M:%S")
        time2 = datetime.strptime(next_point.time, "%H:%M:%S")

        time1 = timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
        time2 = timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second)

        delta = datetime.strptime(str(time2 - time1), "%H:%M:%S")
        delta = delta.second

        sum2 += delta * point.methane

    if sum1 < sum2:
        print(f"Percent change across samples (1/2): {round(sum1 * 100 / sum2, 2)}%")
    else:
        print(f"Percent change across samples (2/1): {round(sum2 * 100 / sum1), 2}%")

    print(sum1, sum2)


def comparative_calibration(dataframe1, dataframe2, calibrate_until=bromoformination_index):
    # Calculate calibration factor for the methane data.
    methane1 = dataframe1.methane.to_list()[:calibrate_until]
    methane2 = dataframe2.methane.to_list()[:calibrate_until]

    methane_normalization_factor = sum(methane1) / sum(methane2)

    # Calculate calibration factor for the hydrogen data.
    hydrogen1 = dataframe1.hydrogen.to_list()[calibrate_until:]
    hydrogen2 = dataframe2.hydrogen.to_list()[calibrate_until:]

    hydrogen_normalization_factor = sum(hydrogen1) / sum(hydrogen2)

    # df2 methane data will be calibrated to have the same average of first five values
    dataframe2['methane'] = dataframe2['methane'].apply(lambda x: x * methane_normalization_factor)

    # df2 hydrogen data will be calibrated to have the same average of first five values
    dataframe2['hydrogen'] = dataframe2['hydrogen'].apply(lambda x: x * hydrogen_normalization_factor)


def max_delta_analysis(dataframe1, dataframe2, delta_after=bromoformination_time):
    list_of_ones = []
    list_of_twos = []

    for i in dataframe1: list_of_ones.append(1)
    for i in dataframe2: list_of_twos.append(2)

    dataframe1['sensor'] = list_of_ones
    dataframe2['sensor'] = list_of_twos

    df = pd.concat(dataframe1, dataframe2)
    df.head(5)
    df = df.reset_index(drop=True)

    bromoformination_dateTime = datetime.strptime(bromoformination_time, "%H:%M:%S")

    droplist = []
    for data in df:  # Filter out the values before bromoformination
        dataTime = datetime.strptime(df.time, "%H:%M:%S")
        delta = bromoformination_dateTime - dataTime

        if delta.days == -1:
            droplist.append(data.index)

    df = df.drop(droplist)
    df = df.reset_index(drop=True)

    # separate df's again
    # get low points of bromoforminated sensor
    # compare it to the points in the other sensor dataset


def threshold(dataframe):
    # Apply thresholds to dataframe for plot readability.
    droplist = dataframe[(dataframe.methane < 000) |
                         (dataframe.hydrogen < 000) |
                         (dataframe.temperature < 20) |
                         (dataframe.humidity < 20) |
                         (dataframe.methane > 1023) |
                         (dataframe.hydrogen > 1023)].index

    dataframe = dataframe.drop(droplist)
    dataframe = dataframe.reset_index(drop=True)  # Re-index after removing values.
    return dataframe


def antialiasing(dataframe, rolling_avg):
    toPlot = pd.DataFrame({'methane': x_moving_average(dataframe.methane, rolling_avg),
                           'hydrogen': x_moving_average(dataframe.hydrogen, rolling_avg),
                           'time': dataframe.time,
                           'humidity': dataframe.humidity,
                           'temperature': dataframe.temperature},
                          columns=['methane', 'hydrogen', 'time', 'humidity', 'temperature'])
    return toPlot


def match_timeseries(dataframe1, dataframe2):
    start = "The lowest value from both datasets."
    end = "The highest value from both datasets."

    methane1_list = []
    methane2_list = []
    time_list = []

    for x in tqdm(range(0, (end - start).seconds)):

        time_to_add = start + datetime.timedelta(seconds=x)
        time_to_add = time_to_add.strftime("%H:%M:%S")

        if time_to_add in dataframe1.time.to_list() \
                and time_to_add in dataframe2.time.to_list():

            filter = time_to_add
            filtered_value1 = dataframe1[(dataframe1['time'] == filter)].iloc[0].methane
            filtered_value2 = dataframe2[(dataframe2['time'] == filter)].iloc[0].methane

            methane1_list.append(filtered_value1)
            methane2_list.append(filtered_value2)
            time_list.append(time_to_add)

        elif time_to_add not in dataframe1.time.to_list() \
                and time_to_add in dataframe2.time.to_list():

            filtered_value2 = dataframe2[(dataframe2['time'] == time_to_add)].iloc[0].methane

            methane1_list.append(0)
            methane2_list.append(filtered_value2)
            time_list.append(time_to_add)

        elif time_to_add not in dataframe2.time.to_list() \
                and time_to_add in dataframe1.time.to_list():
            filtered_value1 = dataframe1[(dataframe1['time'] == time_to_add)].iloc[0].methane

            methane1_list.append(filtered_value1)
            methane2_list.append(0)
            time_list.append(time_to_add)

    new_df = pd.DataFrame({"methane1": methane1_list,
                           "methane2": methane2_list,
                           "time": time_list})

    methane1_array = zip(methane1_list, time_list)
    methane2_array = zip(methane2_list, time_list)

    print(list(methane1_array))
    print(list(methane2_array))

    new_df.to_csv("matched_methane.csv")  # Doesnt work properly


def linearize_zero_gaps(list_to_linearize):  #  to fill in the gap in a list, draws a line between gapped values
    for i in range(1, len(list_to_linearize)):
        if list_to_linearize[i] == 0:
            line_start = list_to_linearize[i - 1]
            for j in range(i + 1, len(list_to_linearize)):
                print(j)
                if list_to_linearize[j] != 0:
                    line_end = list_to_linearize[j]
                    height = line_end - line_start
                    width = j - i
                    slope = height / width
                    break
                else:
                    j += 1
            for k in range(i, j):
                list_to_linearize[k] = line_start + slope * (k - i)
                print(line_start, slope, (k - i))
        i += 1


if __name__ == "__main__":
    sensor1 = Analysis(df1, False, True, start_index, end_index)
    sensor2 = Analysis(df2, False, True, start_index, end_index)
    print(sensor1.data, sensor2.data)
    comperative_plot(sensor1.data, sensor2.data)
