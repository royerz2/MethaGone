import numpy as np
import serial
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
import seaborn as sns
import pandas as pd
import csv
import os
import time
from datetime import datetime
import matplotlib.ticker as mticker



plt.style.use

df1 = pd.DataFrame(data=pd.read_csv("sensor1.csv"))
df2 = pd.DataFrame(data=pd.read_csv("sensor2.csv"))


def assign_arrays(dataframe):

    methane = np.array(dataframe["methane"])
    hydrogen = np.array(dataframe["hydrogen"])
    humidity = np.array(dataframe["humidity"])
    temperature = np.array(dataframe["temperature"])
    time = np.array(dataframe["time"])

    return methane, hydrogen, humidity, temperature, time

methane1, hydrogen1, humidity1, temperature1, time1 = assign_arrays(df1)
methane2, hydrogen2, humidity2, temperture2, time2 = assign_arrays(df2)

fig, ax = plt.subplots()


myLocator = mticker.MultipleLocator(50)

plt.plot_date(time1, methane1)
ax.xaxis.set_major_locator(myLocator)


fig.autofmt_xdate()
plt.tight_layout()

plt.show()

