import pymysql
import csv

connection = pymysql.connect(host='localhost',     #'sql11.freesqldatabase.com',
                                 user='root',          #'sql11189253',
                                 password='root',      #'HttzudApwV',
                                 db='stocks',           #'sql11189253',
                                 charset='utf8mb4',
                                 autocommit=True,
                                 cursorclass=pymysql.cursors.DictCursor)

def import_csv():
    with open('../announcement_dates/announcement_date_data_export.csv', 'rU') as f:
        with connection.cursor() as cursor:
            csv_data = csv.reader(f)
            for row in csv_data:
                cursor.execute('INSERT INTO tickers(ticker_name,announcement_date)''VALUES(%s, %s)',row)
        connection.commit()

# def insert():
#     try:
#         with connection.cursor() as cursor:
#             sql = "INSERT INTO tickers (ticker_name, announcement_date, close_price) VALUES ('wix','2017-11-08',60.08)"
#             cursor.execute(sql)
#             connection.commit()
#     except Exception:
#         print Exception

# def select(ticker_id):
#     try:
#         with connection.cursor() as cursor:
#             # sql = "SELECT firstName, lastName, age FROM persons"
#             sql = "SELECT * FROM tickers WHERE ticker_id = '{}'".format(ticker_id)
#             cursor.execute(sql)
#             results = cursor.fetchall()
#         print results
#     except Exception:
#         print Exception
#
# def delete():
#     try:
#         with connection.cursor() as cursor:
#             sql = "DELETE FROM persons WHERE announcement_date = ''"
#             cursor.execute(sql)
#             connection.commit()
#     except Exception:
#         print Exception
#
#
# def update():
#     try:
#         with connection.cursor() as cursor:
#             sql = "UPDATE persons SET ticker_id = 6 WHERE ticker_id = 7"
#             cursor.execute(sql)
#             connection.commit()
#     except Exception:
#         print Exception


import_csv()
