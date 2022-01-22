import pandas as pd
import numpy as np
from tqdm import tqdm

start_point = 1758

df1 = pd.read_csv("sensor1.csv")
df2 = pd.read_csv("sensor2.csv")

print(df1.size)

print(df1[(df1.methane > 1023) | (df1.hydrogen > 1023)])

df1 = df1.drop(df1[(df1.methane > 1023) | (df1.hydrogen > 1023)].index)

print(df1.head(50))

df1 = df1.reset_index(drop=True)

print(df1.head(50))

for i in tqdm(range(1, len(df1.index))):
    df1.iloc[i].name = df1.iloc[i].name + 1
    print(df1.iloc[i].name)




print(df1)