import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.pyplot import figure
from tqdm import tqdm

df1 = pd.read_csv("sensor1.csv")  # Assigns sensor data from probe 1 to variable.

#################################################### PARAMETERS #######################################################

start_index = 1758  # Set to zero to begin from initial entry.
end_index = len(df1.index)  # Set to len(df1.index) to go to the end.
applyThreshold = True  # See the plot with threshold values, then turn to true.
applyAntiAliasing = False  # See the plot before Anti-Aliasing, then turn to true.

plt.style.use("seaborn")  # Sets design language of the plots.
myLocator = mticker.MultipleLocator(100)  # Sets x axis timestamp frequency.


#######################################################################################################################


class Analysis:  # Defines analysis algorithm for data object. Acts as a meta-function.
    def __init__(self, dataframe, rolling_avg=5, antialiasing=False, threshold=False, start=0, end=9999999):
        self.data = dataframe.drop(index=df1.index[:start],
                                   axis=0)  # Sets min point of data range to be analyzed.

        self.data = self.data.drop(index=df1.index[(end + 1):],
                                   axis=0)  # Sets max point of data range to be analyzed.

        self.data = self.data.reset_index(drop=True)  # Reset index to prevent gaps that raise errors during averaging.

        if antialiasing:
            # Apply thresholds to dataframe for plot readability.
            droplist = self.data[(self.data.methane < 200) |
                                 (self.data.hydrogen < 200) |
                                 (self.data.temperature < 20) |
                                 (self.data.humidity < 20) |
                                 (self.data.methane > 1023) |
                                 (self.data.hydrogen > 1023)].index

            self.data = self.data.drop(droplist)

            self.data = self.data.reset_index(drop=True)  # Re-index after removing values.

        print('Data description prior to data wrangling')
        df_describe(self.data)

        print(df1)  # Provides overview of the dataframe to be analyzed.

        df_describe(self.data)  # Describes general aspects of the data; Var, Avg, Corr.

        # Applies rolling average method to smoothen the data.
        if threshold:

            self.toPlot = pd.DataFrame({'methane': x_moving_average(self.data.methane, rolling_avg),
                                        'hydrogen': x_moving_average(self.data.hydrogen, rolling_avg),
                                        'time': self.data.time,
                                        'humidity': self.data.humidity,
                                        'temperature': self.data.temperature},
                                       columns=['methane', 'hydrogen', 'time', 'humidity', 'temperature'])

            print(self.toPlot.head(5))

            request_plot(self.toPlot, 'Sensor 1 Data')  # Applies rolling average method to smoothen the data.

        else:
            request_plot(self.data, 'Sensor 1 Data')  # Gets plot.

        print('Data description after data wrangling')
        df_describe(self.data)  # Does statistical analysis.


def x_moving_average(raw_array, x):
    if (x % 2) == 0:  # Check if x is odd for proper functionality.
        print("{0} is Even number".format(x))
        print("Rolling average value should be an odd number.")
        raise EOFError

    averaged_array = np.array([])

    span = int(x / 2 - 0.5)  # How many data from left and right of a data to average.

    # Un-averageable points set aside to add later
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


def anti_aliasing(dataframe):
    for i in tqdm(range(start_index, end_index)):

        # If there are any rows that spike 100 up or down delete them.
        if (abs(dataframe.hydrogen[i] - dataframe.hydrogen[i + 1]) > 100) or \
                (abs(dataframe.hydrogen[i + 1] - dataframe.hydrogen[i + 2]) > 100) or \
                (abs(dataframe.methane[i] - dataframe.methane[i + 1]) > 100) or \
                (abs(dataframe.methane[i + 1] - dataframe.methane[i + 2]) > 100):
            dataframe = dataframe.drop(dataframe[i + 1])


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
    figure(figsize=(8, 6), dpi=80)
    plt.show()


def df_describe(dataframe):
    df = dataframe

    plt.matshow(df.corr())
    plt.title("Correlation Matrix")
    plt.show()

    df.dropna(inplace=True)

    include = ['object', 'float', 'int']

    desc = df.describe(include=include)

    print(desc)


# Create data analysis instance of df1, with 5-point moving average
plot = Analysis(df1, 5, applyAntiAliasing, applyThreshold, start_index, end_index)
