import pymysql
import openpyxl
from pymysql.cursors import DictCursor
import datetime
from datetime import datetime, timedelta


def get_product():
    year, month = str(datetime.now())[:7].split("-")
    month = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"][int(month) - 1]
    connection = pymysql.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack',
                                 cursorclass=DictCursor, port=3306)
    queue = f"""SELECT ProductId FROM COLs WHERE LatestDesiredDeliveryDate like '{'_-' + str(month) + '.-' + str(
        year)}' or LatestDesiredDeliveryDate like '{'__-' + str(month) + '.-' + str(year)}'"""  # SQL запрос
    cursor = connection.cursor()
    cursor.execute(queue)
    ans = [i["ProductId"] for i in cursor.fetchall()]
    product_count = dict()
    for i in set(ans):
        product_count[i] = ans.count(i)
    top_5 = [i for i in reversed(sorted(product_count.values()))][:5]
    res = dict()
    print(1)
    connection = pymysql.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack',
                                 cursorclass=DictCursor, port=3306)
    cursor = connection.cursor()
    for i in product_count.keys():
        if product_count[i] in top_5:
            queue = f"""SELECT Название_продукта FROM Supply_orders  WHERE ProductId = '{i}'"""
            cursor.execute(queue)
            a = cursor.fetchone()
            res[product_count[i]] = a['Название_продукта']
    return res


def get_cols():
    year, month = str(datetime.now())[:7].split("-")
    month = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"][int(month) - 1]
    connection = pymysql.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack', cursorclass=DictCursor, port=3306)
    queue = f"""SELECT LatestDesiredDeliveryDate FROM COLs WHERE LatestDesiredDeliveryDate like '{'_-' + str(month) +'.-' + str(year)}' or LatestDesiredDeliveryDate like '{'__-' + str(month) +'.-' + str(year)}'"""# SQL запрос
    cursor = connection.cursor()
    cursor.execute(queue)
    ans = [i["LatestDesiredDeliveryDate"] for i in cursor.fetchall()]
    res = dict()
    for i in set(ans):
        res[i] = ans.count(i)
    return res
print(get_product())