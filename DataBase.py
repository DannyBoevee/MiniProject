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

    def getGastLijst(self, date):
        global aanbieder
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM aanwezichheidBijFilm WHERE aanbieder = %s AND dag = %s  ORDER  BY film"
                cursor.execute(sql, (aanbieder, date))
                result = cursor.fetchall()
            return result
        except Exception as e:
            print('Fout bij het ophalen van gasten')
            return False
