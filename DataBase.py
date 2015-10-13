import pymysql.cursors

userid = 0


class DataBase:
    connection = None

    def __init__(self):
        # Connect to the database
        try:
            self.connection = pymysql.connect(host='cloud.d-consultancy.nl',
                                              user='mini',
                                              password='123123',
                                              db='thuisbios',
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print('Fout bij de verbinding van de Mysql server')

    def checkLogin(self, username, password):
        global userid
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s And password = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
            if result == None:
                return False
            else:
                userid = result['id']
                return True
        except Exception as e:
            print('Fout bij het verkrijgen van de user')
            return False

    def seveFilmId(self, filmId):
        global userid
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO usersFilms (userId, filmId) VALUES (%s, %s)"
                cursor.execute(sql, (userid, filmId))
            self.connection.commit()
        except Exception as e:
            print('Fout bij het opslaan van de film id')
            return False
