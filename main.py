from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.finance import candlestick_ohlc
import pandas_datareader.data as web
import matplotlib.dates as mdates
import numpy as np

# dateOffsetObject
# returns list of stocks at key dates relative to announcement date

def get_stock_prices_at_key_dates(list_of_stock_price_data, announcement_date):

    stock_prices_at_key_dates_dictionary = {}
    key_date_intervals = [1, 3, 5, 10, 30] # of days since announcement date

    for stock in list_of_stock_price_data:
        stock_price = stock['Adj Close']
        # convert the date from a pandas object to a python object
        date_of_stock = stock['Date'].to_pydatetime()
        days_since_announcement_date = find_days_since_announcement_date(announcement_date, date_of_stock)

        if days_since_announcement_date in key_date_intervals:
            key_date = date_of_stock
            print "key_date", key_date
            stock_prices_at_key_dates_dictionary[days_since_announcement_date] = stock_price
            # stock_prices_at_key_dates_dictionary['date'] = announcement_date

    print "stock_prices_at_key_dates_dictionary", stock_prices_at_key_dates_dictionary
    return stock_prices_at_key_dates_dictionary

def get_stock_prices_from_csv(file_name):
    df = pd.read_csv(file_name, parse_dates=True, index_col=0)
    df = df.reset_index()
    # Convert dataframe to list of dictionaries
    list_of_stock_price_data = df.to_dict('records')

    print "list_of_stock_price_data", list_of_stock_price_data
    return list_of_stock_price_data

def find_days_since_announcement_date(announcement_date, date_of_stock):
    number_of_days_difference = (date_of_stock - announcement_date).days

    return number_of_days_difference

#TODO
def get_min_and_max_stock_prices(stock_prices_at_key_dates_relative_to_announcement_date, stock_prices_for_announcement_dates):
    min_key_date, max_key_date = '',''
    # 1, 5, 10, 30 day after -->table with data for each day
    # ex: 63.90 at 7/27/17 --> 10 days later high was 78.84 and low was 67
    # if 78 - 63.9 >0, return (max/63.9-1) else return price at announcement (min/63.9 -1)

    for stock_price_key_date in stock_prices_for_announcement_dates:
        stock_prices_at_key_dates_values = stock_prices_for_announcement_dates
        print "stock_prices_at_key_dates_values", stock_prices_at_key_dates_values
        print "stock_prices_for_announcement_dates", stock_prices_for_announcement_dates
        max_key_date = max(stock_prices_at_key_dates_values)
        min_key_date = min(stock_prices_at_key_dates_values)
        print "stock_price_key_date", stock_price_key_date

    print "min_key_date", min_key_date
    print "max_key_date", max_key_date

def main():
    list_of_stock_price_data = get_stock_prices_from_csv('wix_prices.csv')

    # formatted_string_date = str(dates)[1:-1]
    # announcement_dates = [[datetime(2014, 11, 5)], [datetime(2014, 12, 5)]]
    announcement_dates = [datetime(2014,11,5), datetime(2015,2,11), datetime(2015,5,6),
                         datetime(2015,8,5), datetime(2015,11,4), datetime(2016,2,10),
                         datetime(2016,5,4), datetime(2016,7,27), datetime(2016,11,10),
                         datetime(2017,2,15), datetime(2017,5,10), datetime(2017,7,27), datetime(2017,11,8)]


    #time series-->index of window easier with time series (revolving time window)
    print "announcement_dates", announcement_dates

    stock_prices_for_announcement_dates = {}
    stock_prices_at_key_dates_relative_to_announcement_date = {}

    for announcement_date in announcement_dates:
        stock_prices_at_key_dates_relative_to_announcement_date = get_stock_prices_at_key_dates(list_of_stock_price_data, announcement_date)
        print "stock_prices_at_key_dates_relative_to_announcement_date", stock_prices_at_key_dates_relative_to_announcement_date

        stock_prices_for_announcement_dates[announcement_date] = stock_prices_at_key_dates_relative_to_announcement_date

    # TODO: Call function to run data comparison to get min/max
    get_min_and_max_stock_prices(stock_prices_at_key_dates_relative_to_announcement_date, stock_prices_for_announcement_dates)

main()

# dates = ['2014-11-05','2015-02-11','2015-05-06','2015-08-05','2015-11-04','2016-02-10','2016-05-04',
#          '2016-07-27','2016-11-10','2017-02-15','2017-05-10','2017-07-27', '2017-11-08']
# dates = ['2014,11,05','2015,02,11','2015,05,06','2015,08,05','2015,11,04','2016,02,10','2016,05,04',
#          '2016,07,27','2016,11,10','2017,02,15','2017,05,10','2017,07,27', '2017,11,08']
# dates = ['20141105', '20150211', '20150506', '20150805', '20151104', '20160210', '20160504',
#          '20160727', '20161110', '20170215', '20170510', '20170727', '20171108']
# dates = [(2014,11,5),(2015,2,11),(2015,5,6),(2015,8,5),(2015,11,4),(2016,2,10),(2016,5,4),(2016,7,27),
#          (2016,11,10),(2017,2,15),(2017,5,10),(2017,7,27), (2017,11,8)]
dates = [[2014,11,5],[2015,2,11],[2015,5,6],[2015,8,5],[2015,11,4],[2016,2,10],[2016,5,4],[2016,7,27],
         [2016,11,10],[2017,2,15],[2017,5,10],[2017,7,27], [2017,11,8]]


