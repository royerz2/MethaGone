import numpy as np
import pandas as pd

df1 = pd.DataFrame(data=pd.read_csv("sensor1.csv"))

date_filler()

def date_filler(gapped_date):
    filled_date = np.array([])

    max_ = gapped_date.max()
    min_ = gapped_date.min()

    for i in range

        filled_date = np.append(filled_date, added_date)

    return filled_date
