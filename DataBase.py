import pymysql.cursors

userid = 0


class DataBase:
    def __init__(self):
        # Connect to the database
        """self.connection = pymysql.connect(host='localhost',
                                          user='thuisbios',
                                          password='Python',
                                          db='thuisbios',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)"""
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='',
                                          db='thuisbios',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def checkLogin(self, username, password):
        global userid
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s And password = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
        if result == None:
            return False
        else:
            userid = result['id']
            return True