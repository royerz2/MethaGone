import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta
import pendulum
from tqdm import tqdm

df = pd.DataFrame(data=pd.read_csv("sensor1.csv"))


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

            time_list[2] = str(int(time_list[2])+1)

        elif int(time_list[2]) == 59 and int(time_list[1]) < 59:

            time_list[2] = "00"
            time_list[1] = str(int(time_list[1])+1)

        elif int(time_list[2]) == 59 and int(time_list[1]) == 59 and int(time_list[0]) < 23:

            time_list[2] = "00"
            time_list[1] = "00"
            time_list[0] = str(int(time_list[0])+1)

        elif int(time_list[2]) == 59 and int(time_list[1]) == 59 and int(time_list[0]) == 23:

            time_list[2] = "00"
            time_list[1] = "00"
            time_list[0] = "00"

        else:
            raise Warning

        added_time = time_list[0].zfill(2) + ":" + time_list[1].zfill(2) + ":" + time_list[2].zfill(2)

        filled_time = np.append(filled_time, added_time)

    return filled_time


print(time_filler(df["time"]))
