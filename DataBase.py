import pymysql.cursors

aanbieder = ''


class DataBase:
    connection = None

    def __init__(self):
        # Connect to the database
<<<<<<< HEAD
        """self.connection = pymysql.connect(host='localhost',
                                          user='thuisbios',
                                          password='Python',
                                          db='thuisbios',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)"""
        self.connection = pymysql.connect(host='cloud.d-consultancy.nl',
                                          user='mini',
                                          password='123123',
                                          db='thuisbios',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
=======
        try:
            self.connection = pymysql.connect(host='cloud.d-consultancy.nl',
                                              user='mini',
                                              password='123123',
                                              db='thuisbios',
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print('Fout bij de verbinding van de Mysql server')
>>>>>>> 1d6897c0051e85356a7d7d8ac8f76441705e0a9e

    def checkLogin(self, username, password):
        global aanbieder
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM aanbieder WHERE username = %s And password = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
            if result == None:
                return False
            else:
                userid = result['username']
                return True
        except Exception as e:
            print('Fout bij het verkrijgen van de user')
            return False

    def saveFilm(self, filmId, aanbieder, date):
        global userid
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO aanwezichheidBijFilm (film, aanbieder, dag) VALUES (%s, %s, %s)"
                cursor.execute(sql, (filmId, aanbieder, date))
            self.connection.commit()
            return True
        except Exception as e:
            print('Fout bij het opslaan van de film')
            return False
