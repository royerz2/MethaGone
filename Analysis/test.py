import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("sensor1.csv")

print(df.corr())

plt.matshow(df.corr())
plt.title("Correlation Matrix")
plt.show()

df.dropna(inplace=True)

include = ['object', 'float', 'int']

desc = df.describe(include=include)

print(desc)
