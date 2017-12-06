from datetime import datetime, timedelta
import sys
import pandas as pd
from pandas.tseries.offsets import BDay
import csv
from pandas_datareader import data, wb
import glob, os
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
# from pandas_datareader import data

tickers = ['amzn']

def get_stock_prices_from_yahoo():
    data_source = 'yahoo'
    start_date = '2014/11/05'
    end_date = '2017/11/27'

    company_data = data.DataReader(tickers, data_source, start_date, end_date)
    df = company_data.ix['Close']

    #only pull weekdays
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

    #Reindexing will insert missing values (NaN) for the dates that were not present
    # in the original set. To cope with this, we can fill the missing by replacing them
    # with the latest available price for each instrument.
    df = df.reindex(all_weekdays)
    df = df.fillna(method='ffill')

    # pd.to_datetime(df.index,format=date_format)

    file_name = '{ticker}_price_data.csv'.format(ticker='_'.join(tickers))
    df.to_csv(file_name, sep='\t')

    # print "columns: ", df.columns[0]
    # print "index: ", df.index

    df = df.reset_index()
    df = df.rename(columns={'index':'Date', tickers[0]: 'Close'})

    generate_announcement_date_masks(df)
    return df

#keep date formatting consistent with CSV
DATE_FORMAT_STRING = "%d/%m/%y"
str_to_datetime = lambda s: pd.datetime.strptime(s, DATE_FORMAT_STRING)

def get_stock_prices_from_csv():
    df = pd.read_csv('WIX_share_prices.csv', parse_dates=['Date'], date_parser=str_to_datetime, index_col=0)
    df = df.reset_index()
    print "df", df
    #pd.to_datetime(df.Date)
    #df.Date = pd.to_datetime(df.Date, format=DATE_FORMAT_STRING)

    generate_announcement_date_masks(df)
    return df

def create_mask(date, df):
    if not isinstance(date, datetime):
        raise Exception('date passed into create_mask() was not python datetime')

    print df.head()
    mask = (df.Date.dt.year == date.year) & (df.Date.dt.month == date.month) & (df.Date.dt.day == date.day)
    # print "mask", mask
    return mask

def generate_announcement_date_masks(df):
    dates = ['2014/11/05','2015/02/11','2015/05/06','2015/08/05','2015/11/04','2016/02/10','2016/05/04',
              '2016/07/27','2016/11/10','2017/02/15','2017/05/10','2017/07/27', '2017/11/08']

    announcement_date_string_format = '%Y/%m/%d'
    announcement_dates = pd.to_datetime(dates, format=announcement_date_string_format)

    # announcement_dates = [str_to_datetime(date) for date in dates]
    # print('announcement_dates:', announcement_dates)

    #fixing the first date
    #print 'df at location 772', df.iloc[[770]]

    announcement_date_masks = [create_mask(announcement_date, df) for announcement_date in announcement_dates]
    # print "announcement_date_masks", announcement_date_masks #type = 'list'

    # announcement_date_mask = [True, False] ==> mask of all rows in the df
    announcement_date_mask = reduce(lambda x, y: x | y, announcement_date_masks, False)
    # print "announcement_date_mask", df[announcement_date_mask]

    get_stock_data_on_key_dates(df[announcement_date_mask], df)

    return announcement_date_mask

def get_stock_data_on_key_dates(announcement_date_mask, df):

    key_date_intervals = [0, 1, 3, 5, 10, 30]
    output_data = {}

    # iterate through each announcement date
    for index, row in announcement_date_mask.iterrows():
        #index number for each announcement date
        # print "index", index

        #data for each announcement date
        # print "row", row

        all_key_dates_data_for_announcement_date = {}
        # all_key_dates_data_for_announcement_date = get_data_for_announcement_date(df, announcement_date)

        # iterate through each interval element
        for key_date_offset in key_date_intervals:
            announcement_date = row['Date']

            # type = <class 'pandas._libs.tslib.Timestamp'>
            # key_date_for_announcement_date = announcement_date + timedelta(days=key_date_offset)

            #account for business days
            key_date_for_announcement_date_business_days = announcement_date + BDay(key_date_offset)
            print "key_date_for_announcement_date_business_days", key_date_for_announcement_date_business_days

            key_date_mask = create_mask(key_date_for_announcement_date_business_days, df)
            # print "key_date_mask",key_date_mask

            # type = 'pandas.core.series.Series'
            #data for each key date
            row_for_key_date_for_announcement_date = df[key_date_mask]
            # print "row_for_key_date_for_announcement_date", row_for_key_date_for_announcement_date

            #convert the list of of row_for_key_date_for_announcement_date to a dictionary
            key_date_list = row_for_key_date_for_announcement_date.to_dict('records')

            #only have one row in the df
            if len(key_date_list) == 0:
                # If no value for the key date then continue to the next one
                continue

            #converting each key_date_list to a dictionary
            key_date_dict = key_date_list[0]
            # print "key_date_dict", key_date_dict

            #dictionary with keys as offset day and value as dictionary with all data
            all_key_dates_data_for_announcement_date[key_date_offset] = key_date_dict
            # print "all_key_dates_data_for_announcement_date", all_key_dates_data_for_announcement_date

        format_announcement_date_for_output = lambda d: str(d)
        formatted_announcement_date = format_announcement_date_for_output(announcement_date)

        output_data[formatted_announcement_date] = all_key_dates_data_for_announcement_date
        # print "output_data", output_data

    analyze_results(output_data)
    return output_data

def create_date_mask(initial_date, offset, df):
    # bday_us = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    desired_date_with_business_days = initial_date + BDay(offset)

    # desired_date_with_business_days = initial_date + bday_us(offset)
    print "desired_date_with_business_days", desired_date_with_business_days
    # desired_date = initial_date + timedelta(days=offset)

    datetime_index = pd.DatetimeIndex(df.Date)
    mask_offset_comparison = pd.offsets.Day(offset) + initial_date

    date_mask = (datetime_index >= desired_date_with_business_days) & (datetime_index <= mask_offset_comparison)

    print "date_mask", date_mask
    return date_mask

def create_csv_row(announcement_date, key_date_stocks):
    # print "key_date_stocks", key_date_stocks
    # key_date_stocks: dictionary for each announcement date with offset as key and data as values

    '''
    :param announcement_date:
    :param key_date_stocks: {} --> {key_date_offset: {'Volume': 100,'Adj. Closed': 22.3... }
    :return: {announcement_date: announcement_date, price_at_day_X: 5.4, price_diff_at_day_x: -0.1, price_at_day_Y: 6.3, ...}
    '''
    announcement_date_price = round(key_date_stocks[0]['Close'],2)

    row = {
        'announcement_date': announcement_date,
        'announcement_date_close_price': announcement_date_price,
    }

    #price_at_offset_day = get_close_price(key_date_stock)
    #price_percent_difference_at_offset_day = get_price_difference(price_at_offset_day, announcement_date_price)
    #price_absolute_difference_at_offset_day = get_price_difference(price_at_offset_day, announcement_date_price)

    for offset, stock_data in key_date_stocks.iteritems():
        # each offset interval
        # print "offset", offset

        # data for each individual offset
        # print "stock_data", stock_data

        if (offset == 0):
            #skip the actual announcement date
            continue

        price_at_day_offset_key_string = 'price_at_day_{offset}'.format(offset=offset)
        price_absolute_difference_key_string = 'absolute_price_difference_at_day_{offset}'.format(offset=offset)
        price_percent_difference_key_string = 'percent_price_difference_at_day_{offset}'.format(offset=offset)

        # add data_for_key_date to row
        stock_price_key_date_close = round(stock_data['Close'],2)
        row[price_at_day_offset_key_string] = round(stock_price_key_date_close,2)
        row[price_absolute_difference_key_string] = round(-(announcement_date_price - stock_price_key_date_close),2)
        row[price_percent_difference_key_string] = round(-((float(announcement_date_price - stock_price_key_date_close)/stock_price_key_date_close)) * 100 ,2)

    return row

def analyze_results(output_data):
    '''
    show key date, close price, and % change relative to announcement_date
    column_headings => announcement-date, offset_1, offset_1_%, ...
     list of dictionaries (with same keys) => csv
     output_data = {< announcement_date >: { < key_dateoffset >: stock_object, < key_date_offset_2 >: stock_object}}

    :param output_data:
    :param announcement_date_mask:
    :return:
    '''
    #create list of dictionaries
    output_data_for_csv = []

    for announcement_date, key_date_stocks in output_data.iteritems():

        #key_date_stocks: dictionary for each announcement date with offset as key and data as values
        print "key_date_stocks", key_date_stocks

        # Create one row
        row = create_csv_row(announcement_date, key_date_stocks)
        output_data_for_csv += [row]

    output_results_to_csv(output_data_for_csv)
    return output_data_for_csv

def output_results_to_csv(output_data_for_csv):
    # convert list of dictionaries to df
    df = pd.DataFrame(output_data_for_csv)
    df = df.sort_values(by='announcement_date', ascending=False)
    df.reset_index()


    # output df to csv
    file_name = '{ticker}_stock_price_results.csv'.format(ticker='_'.join(tickers))
    df.to_csv(file_name, index=False)

    ordered_file_name = '{ticker}_stock_price_results_ordered.csv'.format(ticker='_'.join(tickers))

    #re-order CSV columns
    with open(file_name, 'r') as infile, open(ordered_file_name, 'w') as outfile:
        # output dict needs a list for new column ordering
        fieldnames = [
            'announcement_date',
            'announcement_date_close_price',
            'price_at_day_1',
            'absolute_price_difference_at_day_1',
            'percent_price_difference_at_day_1',
            'price_at_day_3',
            'absolute_price_difference_at_day_3',
            'percent_price_difference_at_day_3',
            'price_at_day_5',
            'absolute_price_difference_at_day_5',
            'percent_price_difference_at_day_5',
            'price_at_day_10',
            'absolute_price_difference_at_day_10',
            'percent_price_difference_at_day_10',
            'price_at_day_30',
            'absolute_price_difference_at_day_30',
            'percent_price_difference_at_day_30'
        ]

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)
    combine_all_results_ordered()
    return outfile

def combine_all_results_ordered():
    os.chdir("/Users/Josh/Documents/startup/stock_movements")
    results = pd.DataFrame([])

    for counter, file in enumerate(glob.glob("results_ordered*")):
        name_df = pd.read_csv(file, skiprows=0, usecols=[1, 2, 3])
        results = results.append(name_df)

    results.to_csv("/Users/Josh/Documents/startup/stock_movements/combined_results.csv")


def main():
    get_stock_prices_from_yahoo()
    # get_stock_prices_from_csv()

main()
