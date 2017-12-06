# coding: utf-8
import pandas as pd
df = pd.read_csv("wix_prices.csv")
df.Date=pd.to_datetime(df.Date)


