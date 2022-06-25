import datetime
import pandas as pd
import analysis2 as analyzer
from tqdm import tqdm
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.style.use("seaborn")  # Sets design language of the plots.
myLocator = mticker.MultipleLocator(200)  # Sets x axis timestamp frequency.

dataframe1 = analyzer.threshold(pd.read_csv("p6s1_22_06.csv"))
dataframe2 = analyzer.threshold(pd.read_csv("p6s2_22_06.csv"))

df = dataframe2.append(dataframe1)

start = datetime.datetime.strptime("13:12:50", "%H:%M:%S")
end = datetime.datetime.strptime("16:56:58", "%H:%M:%S")


def linearize_zero_gaps(list_to_linearize):  # to fill in the gap in a list, draws a line between gapped values
    for i in range(1, len(list_to_linearize)):
        if list_to_linearize[i] == 0:
            line_start = list_to_linearize[i - 1]
            for j in range(i + 1, len(list_to_linearize)-37):
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
    return list_to_linearize


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

new_df.to_csv("matched_methane.csv")

fig, (ax1, ax2) = plt.subplots(2)  # Make four subplots.

fig.suptitle("title")
ax1.plot_date(time_list, linearize_zero_gaps(methane1_list),
              linestyle="solid", markersize=0, label="Sensor 1")

ax2.plot_date(time_list, linearize_zero_gaps(methane2_list),
              linestyle="solid", markersize=0, label="Sensor 2")


ax1.xaxis.set_major_locator(myLocator)
ax2.xaxis.set_major_locator(myLocator)
ax1.set_ylim([0, 825])
ax2.set_ylim([0, 825])

plt.gcf().autofmt_xdate()
plt.tight_layout()

ax1.legend()
ax2.legend()

figure(figsize=(8, 6), dpi=800)
plt.show()
