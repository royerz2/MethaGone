import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.ticker as mticker


df1 = pd.read_csv("sensor1.csv")
df2 = pd.read_csv("sensor2.csv")

plt.style.use("seaborn")
myLocator = mticker.MultipleLocator(50)

def x_moving_average(raw_array, x):
    averaged_array = np.array([])
    tba = raw_array[len(raw_array) - x:]

    for i in range(len(raw_array) - x):
        sumlist = []
        for k in range(i+1, i + x + 1):
            sumlist.append(raw_array[k])
        print(sumlist)
        print(sum(sumlist)/x)

        averaged_array = np.append(averaged_array, sum(sumlist)/x)

    averaged_array = np.append(averaged_array, tba)
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

request_plot(df1, "Sensor 1")
request_plot(df2, "Sensor 2")