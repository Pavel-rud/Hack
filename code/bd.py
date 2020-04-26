import pymysql
import openpyxl
from pymysql.cursors import DictCursor
import datetime
from datetime import datetime, timedelta


def get_cols():
    year, month = str(datetime.now())[:7].split("-")
    month = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"][int(month) - 1]
    connection = pymysql.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack', cursorclass=DictCursor, port=3306)
    queue = f"""SELECT * FROM COLs WHERE LatestDesiredDeliveryDate like '{'_-' + str(month) +'.-' + str(year)}' or LatestDesiredDeliveryDate like '{'__-' + str(month) +'.-' + str(year)}'"""# SQL запрос
    cursor = connection.cursor()
    cursor.execute(queue)
    ans = [i["LatestDesiredDeliveryDate"] for i in cursor.fetchall()]
    res = dict()
    for i in set(ans):
        res[i] = ans.count(i)
    return res
