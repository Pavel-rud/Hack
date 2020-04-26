import pymysql
import openpyxl
from pymysql.cursors import DictCursor


class MySQL(): # Функции для подключения и работы с БД

    def connect(host, username, password, dbname): # Создания подключения к БД
        global connection
        connection = pymysql.connect(host, username, password, dbname, cursorclass=DictCursor, port=3306)

    def check_login(login): # Проверка существования логина в системе
        global connection
        queue = """SELECT * FROM `users` WHERE login = '""" + login + """'""" # SQL запрос
        cursor = connection.cursor()
        cursor.execute(queue) # Выполнение SQL запроса
        ans = cursor.fetchone() # Присваивание ответа от выполнения SQL запроса в переменную ans
        try:
            if login == ans['login']: # Попытка проверить существования логина
                return 0 # Возврат "0", как сигнала, что ошибок нет
        except TypeError:
            return 144 # Возврат "145", как сигнала об ошибке "Логина не существует"

    def check_password(login, password): # Проверка пароля к логину
        global connection
        queue = """SELECT * FROM users WHERE login = '""" + login + """'""" # SQL запрос
        cursor = connection.cursor()
        cursor.execute(queue) # Выполнение SQL запроса
        ans = cursor.fetchone() # Присваивание ответа от выполнения SQL запроса в переменную ans
        try:
            if password == ans['password']: # Проверка пароля к аккаунту
                return 0 # Возврат "0", как сигнала, что ошибок нет
            else:
                return 143 # Возврат "143", как сигнала, что пароль неправильный
        except TypeError:
            return 144 # Возврат "145", как сигнала о непредвиденной ошибке



def import_technial_map(name):
    wb = openpyxl.load_workbook(filename=name)
    sheet = wb['Sheet1']

    val = sheet['A1'].value

    vals = []
    n = 0
    while True:
        n += 1
        val = [sheet[f'A{n}'].value, sheet[f'B{n}'].value, sheet[f'C{n}'].value, sheet[f'D{n}'].value,
               sheet[f'E{n}'].value, sheet[f'F{n}'].value, sheet[f'G{n}'].value,
               sheet[f'H{n}'].value, sheet[f'I{n}'].value, sheet[f'J{n}'].value,
               sheet[f'K{n}'].value, sheet[f'L{n}'].value, sheet[f'M{n}'].value,
               sheet[f'N{n}'].value, sheet[f'O{n}'].value, sheet[f'P{n}'].value,
               sheet[f'Q{n}'].value, sheet[f'R{n}'].value, sheet[f'S{n}'].value]
        vals.append(val)
        if val[1] is None:
            break
    vals = vals[1:]
    print(vals)
    for i in range(len(vals)):
        try:
            MySQL.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack')
            queue = """INSERT INTO COLs VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor = connection.cursor()
            cursor.execute(queue, (int(vals[i][0]), str(vals[i][1]), float(vals[i][2]), float(vals[i][3]), float(vals[i][4]), str(vals[i][5]),
                                   str(vals[i][6]), int(vals[i][7]), int(vals[i][8]), str(vals[i][9]), str(vals[i][10]), str(vals[i][11]),
                                   str(vals[i][12]), str(vals[i][13]), str(vals[i][14]), str(vals[i][15]), str(vals[i][16]),
                                   str(vals[i][17]), str(vals[i][18])))
            connection.commit()
            print('yes')
        except Exception as e:
            print(e)


import_technial_map("C:/Users/KSoft.Dev/Desktop/Excel/01.COLs.xlsx")