import requests
import time

class Api:
    api_key = None
    api_web = None

    def __init__(self):
        self.api_key = '9smtwozmiugid4m8m5f9n6g1oaiwt6r4'
        self.api_web = 'http://www.filmtotaal.nl/api/filmsoptv.xml'

    def getApiUrl(self, date, sort):
        return "{0}?apikey={1}&dag={2}&sorteer={3}" . format(self.api_web, self.api_key, date, sort)

    def getCurrentTime(self):
        """
            Krijg huidige datum
        :return:
            Dag - Maand - Jaar
        """
        return time.strftime(time.strftime("%d-%m-%Y"))
