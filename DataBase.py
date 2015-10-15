import pymysql.cursors

aanbieder = ''


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
        global aanbieder
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM aanbieder WHERE username = %s And password = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
            if result == None:
                return False
            else:
                aanbieder = result['username']
                return True
        except Exception as e:
            print('Fout bij het verkrijgen van de user')
            return False

    def saveFilm(self, filmNaam, aanbieder, date, ucode, naam, email):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO aanwezichheidBijFilm (film, aanbieder, dag, uCode, naam, email) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (filmNaam, aanbieder, date, ucode, naam, email))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            print('Fout bij het opslaan van de film')
            return False

    def saveAanbieder(self, film, date):
        global aanbieder
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO aanwezichheidBijAanbieder (film, aanbieder, dag) VALUES (%s, %s, %s)"
                cursor.execute(sql, (film, aanbieder, date))
            self.connection.commit()
            return True
        except Exception as e:
            print('Fout bij het opslaan van de film')
            return False

    def getGastLijst(self, film, date):
        global aanbieder
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM aanwezichheidBijFilm WHERE aanbieder = %s AND dag = %s  AND film = %s"
                cursor.execute(sql, (aanbieder, date, film))
                result = cursor.fetchall()
            return result
        except Exception as e:
            print('Fout bij het ophalen van gasten')
            return False

    def checkFilmAanbieder(self, film, date):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM aanwezichheidBijAanbieder WHERE film = %s AND dag = %s"
                cursor.execute(sql, (film, date))
                result = cursor.fetchone()
            if result == None:
                return False
            else:
                return True
        except Exception as e:
            print('Fout bij het ophalen van de aanbieder')
            return False

    def getFilmAanbieder(self, film, date):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM aanwezichheidBijAanbieder WHERE film = %s AND dag = %s"
                cursor.execute(sql, (film, date))
                result = cursor.fetchone()
            return result['aanbieder']
        except Exception as e:
            print('Fout bij het ophalen van de aanbieder')
            return False

    def checkFilmBijAanbieder(self, film, date):
        global aanbieder
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM aanwezichheidBijAanbieder WHERE film = %s AND dag = %s AND aanbieder = %s"
                cursor.execute(sql, (film, date, aanbieder))
                result = cursor.fetchone()
            if result == None:
                return False
            else:
                return True
        except Exception as e:
            print('Fout bij het ophalen van de aanbieder')
            return False