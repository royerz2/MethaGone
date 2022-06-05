import pandas as pd

df1 = pd.read_csv("sensor1.csv")

print(df1.head(50))

df1 = df1.reset_index(drop=True)

print(df1.head(50))