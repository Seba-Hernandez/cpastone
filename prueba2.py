
import pandas as pd
import numpy as np

df = pd.read_csv("csv_prueba.csv",sep=";")
print(df.describe())

df_describe = df.describe()
print(df_describe)
media = df_describe.loc[["mean"]]
array_media = np.array(media)
print(type(array_media))
print(type(array_media[0][0]))
print(array_media[0][0])
float_media = float(array_media[0][0])
print(float_media)
print(type(float_media))