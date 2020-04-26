from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import os
import time
from datetime import datetime, timezone
import requests
import os
import os.path
import zipfile
import pymysql
import urllib
from pymysql.cursors import DictCursor
from ftplib import FTP
import webbrowser
global path
global file

class SetInit(): # Инициализация настроек
    def __init__(self):
        super().__init__()
        self.pathinit()
        self.download_res()
        self.unzip_res()

    def pathinit(self): # Переход в папку с ресурсами
        global path
        path = os.getenv('APPDATA') + '\\MIPTHack'
        try:
            os.mkdir(path)
            print('LOG (OK): Folder with resources has been created')
        except FileExistsError:
            print('LOG (OK): Folder with resources exists')

    def download_res(self): # Скачивание ресурсов программы
        global path
        try:
            os.chdir(path)
            urllib.request.urlretrieve('http://www.ksoft.online/resources.zip', 'resources.zip')
            print('LOG (OK): Resources has been downloaded')
        except Exception as e:
            print("LOG (ERROR): Resources hasn't been downloaded")
            print(e)

    def unzip_res(self): # Распаковка ресурсов программы
        global path
        try:
            with zipfile.ZipFile("resources.zip", "r") as zip_ref:
                zip_ref.extractall(path)
            os.remove('resources.zip')
            print("LOG (OK): Resources has been unpacked and installed")
        except:
            print("LOG (ERROR): Resources hasn't been unpacked")

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

class Auth(QMainWindow): # Окно авторизации

    def center(self): # Для свободного перемещения окна (Централизация окна)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event): # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event): # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event): # Для свободного перемещения окна
        if self.__press_pos:
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def __init__(self): # Инициализация класса
        super().__init__()
        self.initUI()

    def initUI(self): # Инициализация интерфейса
        def closebtn():
            sys.exit()
        global path
        path = path.replace("\\","/") # Нормализация пути
        uic.loadUi(path + "/auth.ui", self) # Загрузка интерфейса из .ui файла
        self.pwd.setEchoMode(QLineEdit.Password) # Замена знаков в поле "Пароль"
        self.setAttribute(Qt.WA_TranslucentBackground, True) # Удаление рамок окна от ОС
        self.setWindowFlags(Qt.FramelessWindowHint) # Удаление рамок окна от ОС
        #self.setWindowIcon(QIcon(path + '/logo.png'))
        self.setStyleSheet("""background-image:url(""" + path + """/bg-auth.png);""")  # Фон
        self.signin.setStyleSheet("""
                                           QPushButton:!hover { background-image:url(""" + path + """/sign_in.png) }
                                           QPushButton:hover { background-image:url(""" + path + """/sign_in_hover.png) };
                                       """) # Дизайн кнопки "Войти"
        self.reg.setStyleSheet("""
                                           QPushButton:!hover { background-image:url(""" + path + """/register.png) }
                                           QPushButton:hover { background-image:url(""" + path + """/register_hover.png) };
                                       """) # Дизайн кнопки "Регистрация"
        self.closed.setStyleSheet("""
                                                                   QPushButton { border:none; background-image:url(""" + path + """/close.png) }
                                                               """)  # Дизайн кнопки "Закрыть"
        self.loglbl.setStyleSheet('color: #eff5ff; background: #0e1d39;')
        self.pwdlbl.setStyleSheet("color: #eff5ff; background: #0e1d39;")
        self.login.setStyleSheet("""QLineEdit {
                        border: 1px solid #eff5ff;
                        border-radius: 5px;
                        padding: 0 5px;
                        background: #0e1d39;
                        selection-background-color: darkgray;
                        color: #eff5ff;
                        }
                    """) # Дизайн поля "Логин"

        self.pwd.setStyleSheet("""QLineEdit {
                        border: 1px solid #eff5ff;
                        border-radius: 5px;
                        padding: 0 5px;
                        background: #0e1d39;
                        selection-background-color: darkgray;
                        color: #eff5ff;
                        }
                    """) # Дизайн поля "Пароль"

        self.signin.clicked.connect(self.sign_in) # Передача кнопке "Войти" функции sign_in
        #self.reg.clicked.connect(self.register) # Передача кнопке "Регистрация" функции register
        self.closed.clicked.connect(closebtn) # Передача кнопке "Закрыть" задачи закрытия окна

        self.move(QApplication.instance().desktop().screen().rect().center()
                  - self.rect().center()) # Для свободного перемещения окна

    def sign_in(self):
        global connection
        MySQL.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack')
        login = self.login.text()
        pwd = self.pwd.text()
        check1 = MySQL.check_login(login)
        if check1 == 0:
            check2 = MySQL.check_password(login, pwd)
            if check2 == 0:
                print('LOG (OK): Successful enter')
                queue = """SELECT * FROM users WHERE login = '""" + login + """'"""
                cursor = connection.cursor()
                cursor.execute(queue)
                ans = cursor.fetchone()
                if ans['role'] == 'noactive':
                    self.win = Warn('Ваш аккаунт ожидает подтверждения: с Вами свяжется модератор через почту, указанную в ходе регистрации.')
                if ans['role'] == 'moderator':
                    self.win = Dashboard(login)
                    self.win.show()
                    self.close()

            elif check2 == 143:
                print('LOG (ERROR): Incorrect password')
                self.win = Warn(
                    'Вы ввели неверный пароль. Попробуйте ещё раз!')
            elif check2 == 144:
                print('LOG (ERROR): Unexpected error')
                self.win = Warn(
                    'Произошла непредвиденная ошибка!')
        else:
            print("LOG (ERROR): User don't exists")
            self.win = Warn(
                'Пользователя не существует!')

class Warn(QMainWindow): # Окно с сообщением

    def __init__(self, text):  # Инициализация класса
        super().__init__()
        self.ErrorMessage(text)

    def initUI(self, text):
        # Инициализация интерфейса
        print('no interface')

    def ErrorMessage(self, text):
        buttonReply = QMessageBox.critical(self, "Error", text)
        if int(buttonReply) == 1024:
            self.close()

    def okay(self):
        self.close()

class Dashboard(QMainWindow): # Окно авторизации

    def center(self): # Для свободного перемещения окна (Централизация окна)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event): # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event): # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event): # Для свободного перемещения окна
        if self.__press_pos:
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def __init__(self, login): # Инициализация класса
        super().__init__()
        self.initUI(login)

    def initUI(self, login): # Инициализация интерфейса
        def closebtn():
            sys.exit()
        def openurl():
            webbrowser.open('https://tglink.ru/joinchat/CN0_CRu8uxbavoyieVV89w')
        global path
        MySQL.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack')
        queue = """SELECT * FROM users WHERE login = '""" + login + """'"""
        cursor = connection.cursor()
        cursor.execute(queue)
        ans = cursor.fetchone()
        path = path.replace("\\","/") # Нормализация пути
        uic.loadUi(path + "/dashboard.ui", self) # Загрузка интерфейса из .ui файла
        #self.pwd.setEchoMode(QLineEdit.Password) # Замена знаков в поле "Пароль"
        self.setAttribute(Qt.WA_TranslucentBackground, True) # Удаление рамок окна от ОС
        self.setWindowFlags(Qt.FramelessWindowHint) # Удаление рамок окна от ОС
        self.telegram.setStyleSheet("""QPushButton:!hover { border:none; background-image:url(""" + path + """/telegram-fill.png) }
        QPushButton:hover { border:none; background-image:url(""" + path + """/telegram-fill_hover.png) }""")
        self.telegram.clicked.connect(openurl)
        #self.setWindowIcon(QIcon(path + '/logo.png'))
        self.setStyleSheet("""background-image:url(""" + path + """/bg-dashboard.png);""")  # Фон
        try:
            timed = datetime.today()
            self.label.setText(str(timed.strftime("%Y-%m-%d %H:%M ")) + "UTC+" + str(time.timezone / 3600)[1])
        except Exception as e:
            print(e)
        self.name.setText(ans['lastname'] + " " + ans['firstname'])
        if ans['role'] == 'moderator':
            self.name.setText(ans['lastname'] + " " + ans['firstname'] + " (менеджер)")
        self.server_status.setStyleSheet("""color: #eff5ff; background-image:url(""" + path + """/texture.png);""")
        self.server_status.setText("Сервер: 37.140.192.116\nИмя базы данных: u1001983_mipthack\nПодключён: " + str(timed.strftime("%Y-%m-%d %H:%M ")) + "UTC+" + str(time.timezone / 3600)[1] + "\nОшибки: нет")
        try:
            timed2 = datetime(2020, 12, 31, 23, 59, 59)
            timeleft = timed2 - timed
            if int(int(timeleft.seconds / 60) / 60) < 1:
                self.name_4.setText(str(int(int(timeleft.seconds / 60) % 60)) + " минут")
            if int(int(timeleft.seconds / 60) / 60) < 5:
                self.name_4.setText(str(int(int(timeleft.seconds / 60) / 60)) + " часа " + str(int(int(timeleft.seconds / 60) % 60)) + " минут")
            if int(int(timeleft.seconds / 60) / 60) > 5:
                self.name_4.setText(str(int(int(timeleft.seconds / 60) / 60)) + " часов " + str(int(int(timeleft.seconds / 60) % 60)) + " минут")
        except Exception as e:
            print(e)
        self.daytip.setStyleSheet("""color: #eff5ff; background:transparent;""")
        queue = """SELECT * FROM factories WHERE name = '""" + ans['factory'] + """'"""
        cursor = connection.cursor()
        cursor.execute(queue)
        ans = cursor.fetchone()
        self.daytip.setText(ans['day_tip'])
        self.status.setStyleSheet("""color: #eff5ff; background:transparent;""")
        if ans['status'] == 'STOP':
            self.status.setText("""<html><head/><style>*{font-family: "Segoe UI",Frutiger,"Frutiger Linotype","Dejavu Sans","Helvetica Neue",Arial,sans-serif;} p{margin: 0px} .stext{-webkit-transition: All 0.25s ease;-moz-transition: All 0.25s ease;-o-transition: All 0.25s ease;-ms-transition: All 0.25s ease; transition: All 0.25s ease;} .stext:hover{color: black;}</style><body><div class="stext"><p>Нарушений плана не обнаружено</p><p>ID Производства: """ + ans['name'] + """</p><p><br/>Состояние:<span style=" font-weight:500; color: red;"> производство остановлено</span></p></div></body></html>""")
        if ans['status'] == 'WORK':
            self.status.setText("""<html><head/><style>*{font-family: "Segoe UI",Frutiger,"Frutiger Linotype","Dejavu Sans","Helvetica Neue",Arial,sans-serif;} p{margin: 0px} .stext{-webkit-transition: All 0.25s ease;-moz-transition: All 0.25s ease;-o-transition: All 0.25s ease;-ms-transition: All 0.25s ease; transition: All 0.25s ease;} .stext:hover{color: black;}</style><body><div class="stext"><p>Нарушений плана не обнаружено</p><p>ID Производства: """ + ans['name'] + """</p><p><br/>Состояние:<span style=" font-weight:500; color: #3bc229;"> производство запущено</span></p></div></body></html>""")
        self.statusthread = Status_processing(mainwindow=self, factory=ans['name'])
        self.statusthread.start()
        self.status_2.setStyleSheet("color: #eff5ff; background:transparent;")
        if ans['status'] == 'STOP':
            self.status_2.setText("Ваше производство остановлено, аналитика недоступна")
        #self.signin.setStyleSheet("""
        #                         QPushButton:!hover { background-image:url(""" + path + """/sign_in.png) }
        #                            QPushButton:hover { background-image:url(""" + path + """/sign_in_hover.png) };
        #                  """) # Дизайн кнопки "Войти"
        #  self.reg.setStyleSheet("""
        #                                QPushButton:!hover { background-image:url(""" + path + """/register.png) }
        #                                QPushButton:hover { background-image:url(""" + path + """/register_hover.png) };
        #                           """) # Дизайн кнопки "Регистрация"
        self.closed.setStyleSheet("""
                                                                   QPushButton { border:none; background-image:url(""" + path + """/close.png) }
                                                               """)  # Дизайн кнопки "Закрыть"
        #self.loglbl.setStyleSheet('color: #eff5ff; background: #0e1d39; font-family: "Segoe UI Semilight";')
        #self.pwdlbl.setStyleSheet("color: #eff5ff; background: #0e1d39;")
        #self.login.setStyleSheet("""QLineEdit {
        #   border: 1px solid #eff5ff;
        #   border-radius: 5px;
        #    padding: 0 5px;
        #   background: #0e1d39;
        #   selection-background-color: darkgray;
        #   color: #eff5ff;
        #   }
        #    """) # Дизайн поля "Логин"

        #  self.pwd.setStyleSheet("""QLineEdit {
        #   border: 1px solid #eff5ff;
        #     border-radius: 5px;
        #   padding: 0 5px;
        #   background: #0e1d39;
        #  selection-background-color: darkgray;
        #   color: #eff5ff;
        #   }
        #  """) # Дизайн поля "Пароль"

        #self.signin.clicked.connect(self.sign_in) # Передача кнопке "Войти" функции sign_in
        #self.reg.clicked.connect(self.register) # Передача кнопке "Регистрация" функции register
        self.closed.clicked.connect(closebtn) # Передача кнопке "Закрыть" задачи закрытия окна
        self.sessionthread = Time_processing(mainwindow=self)
        self.sessionthread.start()
        self.move(QApplication.instance().desktop().screen().rect().center()
                  - self.rect().center()) # Для свободного перемещения окна

class Status_processing(QThread):
    def __init__(self, mainwindow, factory):
        try:
            super().__init__()
            self.mainwindow = mainwindow
            self.factory = factory
        except Exception as e:
            print(e)

    def run(self):
        while 2 > 1:
            try:
                MySQL.connect('37.140.192.116', 'u1001983_mipt', 'MiptHack', 'u1001983_mipthack')
                queue = """SELECT * FROM factories WHERE name = '""" + self.factory + """'"""
                cursor = connection.cursor()
                cursor.execute(queue)
                ans = cursor.fetchone()
                if ans['status'] == 'STOP':
                    self.mainwindow.status.setText("""<html><head/><style>*{font-family: "Segoe UI",Frutiger,"Frutiger Linotype","Dejavu Sans","Helvetica Neue",Arial,sans-serif;} p{margin: 0px} .stext{-webkit-transition: All 0.25s ease;-moz-transition: All 0.25s ease;-o-transition: All 0.25s ease;-ms-transition: All 0.25s ease; transition: All 0.25s ease;} .stext:hover{color: black;}</style><body><div class="stext"><p>Нарушений плана не обнаружено</p><p>ID Производства: """ + self.factory + """</p><p><br/>Состояние:<span style=" font-weight:500; color: red;"> производство остановлено</span></p></div></body></html>""")
                if ans['status'] == 'WORK':
                    self.mainwindow.status.setText("""<html><head/><style>*{font-family: "Segoe UI",Frutiger,"Frutiger Linotype","Dejavu Sans","Helvetica Neue",Arial,sans-serif;} p{margin: 0px} .stext{-webkit-transition: All 0.25s ease;-moz-transition: All 0.25s ease;-o-transition: All 0.25s ease;-ms-transition: All 0.25s ease; transition: All 0.25s ease;} .stext:hover{color: black;}</style><body><div class="stext"><p>Нарушений плана не обнаружено</p><p>ID Производства: """ + self.factory + """</p><p><br/>Состояние:<span style=" font-weight:500; color: #3bc229;"> производство запущено</span></p></div></body></html>""")
                time.sleep(60)
            except Exception as e:
                print(e)

class Time_processing(QThread):
    def __init__(self, mainwindow):
        try:
            super().__init__()
            self.mainwindow = mainwindow
        except Exception as e:
            print(e)

    def run(self):
        while 2 > 1:
            timed = datetime.today()
            try:
                self.mainwindow.label.setText(str(timed.strftime("%Y-%m-%d %H:%M ")) + "UTC+" + str(time.timezone / 3600)[1])
            except Exception as e:
                print(e)
            try:
                timed2 = datetime(2020, 12, 31, 23, 59, 59)
                timeleft = timed2 - timed
                if int(int(timeleft.seconds / 60) / 60) < 1:
                    self.mainwindow.name_4.setText(str(int(int(timeleft.seconds / 60) % 60)) + " минут")
                if int(int(timeleft.seconds / 60) / 60) < 5:
                    self.mainwindow.name_4.setText(str(int(int(timeleft.seconds / 60) / 60)) + " часа " + str(int(int(timeleft.seconds / 60) % 60)) + " минут")
                if int(int(timeleft.seconds / 60) / 60) > 5:
                    self.mainwindow.name_4.setText(str(int(int(timeleft.seconds / 60) / 60)) + " часов " + str(int(int(timeleft.seconds / 60) % 60)) + " минут")
            except Exception as e:
                print(e)
            time.sleep(1)

if __name__ == '__main__':
    try:
        SetInit()
        app = QtWidgets.QApplication([])
        startwin = Auth()
        startwin.show()
        sys.exit(app.exec_())
    except Exception as er:
        app = QtWidgets.QApplication([])
        win = Warn(er)
        sys.exit(app.exec_())