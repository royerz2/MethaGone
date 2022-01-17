import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta

df = pd.DataFrame(data=pd.read_csv("sensor1.csv"))

date_filler(df["time"])


def date_filler(gaped_date):
    filled_date = np.array([])

    max_ = gaped_date.max()
    min_ = gaped_date.min()

    for i in range(min_, max_):

        filled_date = np.append(filled_date, added_date)

    return filled_date
