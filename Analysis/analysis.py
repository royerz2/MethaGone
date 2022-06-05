import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import pandas as pd
from tqdm import tqdm
import matplotlib.ticker as mticker
import pendulum

plt.style.use("seaborn")
myLocator = mticker.MultipleLocator(50)

df1 = pd.DataFrame(data=pd.read_csv("sensor1.csv"))
df2 = pd.DataFrame(data=pd.read_csv("sensor2.csv"))


def x_moving_average(raw_array, x):

    averaged_array = np.array([])
    tba = raw_array[len(raw_array) - x:]

    for i in range(len(raw_array) - x):
        sumlist = []
        for k in range(i+1, i + x + 1):
            sumlist.append(k)
        print(sumlist)
        print(sum(sumlist)/x)

        averaged_array = np.append(averaged_array, sum(sumlist)/x)

    averaged_array = np.append(averaged_array, tba)
    return averaged_array



def time_filler(gaped_time):
    filled_time = np.array([])

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

        elif int(time_list[2]) == 59 and int(time_list[1]) == 59 and int(time_list[0]) < 23:

            time_list[2] = "00"
            time_list[1] = "00"
            time_list[0] = str(int(time_list[0]) + 1)

        elif int(time_list[2]) == 59 and int(time_list[1]) == 59 and int(time_list[0]) == 23:

            time_list[2] = "00"
            time_list[1] = "00"
            time_list[0] = "00"

        else:
            raise Warning

        added_time = time_list[0].zfill(2) + ":" + time_list[1].zfill(2) + ":" + time_list[2].zfill(2)

        filled_time = np.append(filled_time, added_time)

    return filled_time


def assign_arrays(dataframe):
    methane = np.array(dataframe["methane"])
    hydrogen = np.array(dataframe["hydrogen"])
    humidity = np.array(dataframe["humidity"])
    temperature = np.array(dataframe["temperature"])
    time = np.array(dataframe["time"])

    return methane, hydrogen, humidity, temperature, time


def request_plot():

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Vertically stacked subplots')
    ax1.plot_date(time_filler(time1), methane1,
                  linestyle='solid', label="Sensor 1")
    ax1.plot_date(time_filler(time1), methane2,
                  linestyle='solid', label="Sensor 2")

    ax2.plot_date(time_filler(time1, hydrogen1),
                  linestyle="solid", label="Sensor 1")
    ax2.plot_date(time_filler(time1, hydrogen2),
                  linestyle="solid", label="Sensor 2")

    ax1.xaxis.set_major_locator(myLocator)
    ax2.xaxis.set_major_locator(myLocator)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()

methane1, hydrogen1, humidity1, temperature1, time1 = assign_arrays(df1)
methane2, hydrogen2, humidity2, temperture2, time2 = assign_arrays(df2)

request_plot()





