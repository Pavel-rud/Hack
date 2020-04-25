import pymysql




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


    def sign_in(self):
        global connection
        MySQL.connect('37.140.192.116', 'u1001983_mipthack', 'u1001983_mipt', 'MiptHack')
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
                    self.win.show()
                if ans['role'] == 'moderator':
                    self.win = Moderate(login)
                    self.win.show()
                    self.close()

            elif check2 == 143:
                print('LOG (ERROR): Incorrect password')
                self.win = Warn(
                    'Вы ввели неверный пароль. Попробуйте ещё раз!')
                self.win.show()
            elif check2 == 144:
                print('LOG (ERROR): Unexpected error')
                self.win = Warn(
                    'Произошла непредвиденная ошибка!')
                self.win.show()
        else:
            print("LOG (ERROR): User don't exists")
            self.win = Warn(
                'Пользователя не существует!')
            self.win.show()