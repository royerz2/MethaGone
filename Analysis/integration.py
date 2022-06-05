import numpy as np
import pandas as pd
import pendulum
from tqdm import tqdm

df = pd.read_csv("sensor1.csv")


def time_filler(dataFrame):
    filled_time = []

    gaped_time = dataFrame["time"]

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
            dataFrame = pd.concat([df_line, dataFrame])

    dataFrame["time"] = pd.to_datetime(dataFrame.time, format="%H:%M:%S")
    sorted_data_frame = dataFrame.sort_values(by=['time'], ignore_index=True)

    print(sorted_data_frame)

    return sorted_data_frame


dataFrame = time_filler(df)

