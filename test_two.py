# coding: utf-8
import pandas as pd
df = pd.read_csv("wix_prices.csv")
df.head()
pd.to_datetime(df.Date)
df.Date=pd.to_datetime(df.Date)
df.Date.dt.year
get_ipython().magic(u'save test.py 1-7')
df.Date.dt.day
df.Date + pd.offsets.Day(1)
adf = pd.to_datetime(['2014-11-05'])
adf
announcement_date = adf.values[0]
announcement_date
mask = (df.Date >= announcement_date) & (df.Date <= announcement_date + pd.offset.Day(5))
mask = (df.Date >= announcement_date) 
mask = (pd.DatetimeIndex(df.Date) >= announcement_date)
mask = (pd.DatetimeIndex(df.Date) >= announcement_date) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(5))
mask = (pd.DatetimeIndex(df.Date) >= announcement_date) & (pd.DatetimeIndex(df.Date) <= pd.offset.Day(5))
mask = (pd.DatetimeIndex(df.Date) >= announcement_date) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(5))
mask = (pd.DatetimeIndex(df.Date) >= announcement_date) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(5))
mask = (pd.DatetimeIndex(df.Date) >= announcement_date) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(5)+ announcement_date)
df[mask]
mask_one = (pd.DatetimeIndex(df.Date) >= announcement_date-pd.offsets.Day(1)) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(1)+ announcement_date)
mask_one = (pd.DatetimeIndex(df.Date) >= announcement_date+pd.offsets.Day(-1)) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(1)+ announcement_date)
mask_one = (pd.DatetimeIndex(df.Date) >= announcement_date+pd.offsets.Day(1)) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(1)+ announcement_date)
from datetime import timedelta
d = timedelta(days=-1)
mask_one = (pd.DatetimeIndex(df.Date) >= announcement_date+d) & (pd.DatetimeIndex(df.Date) <= pd.offsets.Day(1)+ announcement_date)
announcement_date + d
announcement_date
mask_one = (df.Date.dt.year == 2014) & (df.Date.dt.month == 11) & (df.Date.dt.day == 6)
df[mask_one]
mask_two = (df.Date.dt.year == 2014) & (df.Date.dt.month == 11) & (df.Date.dt.day == 8)
df[mask_two]
df[mask_one|mask_two]
df[mask_one|mask_two]['Adj Close']
df[mask_one|mask_two]['Adj Close'].min()
df[mask_one|mask_two]['Adj Close'].max()
masks = [mask_one, mask_two]
mask_final = reduce(lambda x,y: x|y, masks, False)
df[mask_final]
mask_final = reduce(lambda x,y: x|y, masks, True)
df[mask_final]
mask_final = reduce(lambda x,y: x|y, masks, False)
