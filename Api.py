import requests
import time

class Api:
    api_key = None

    def __init__(self):
        api_key = '9smtwozmiugid4m8m5f9n6g1oaiwt6r4'
        api_web = 'http://www.filmtotaal.nl/api/filmsoptv.xml?apikey='

    def getCurrentTime(self):
        """
            Krijg huidige datum
        :return:
            Dag - Maand - Jaar
        """
        return time.strftime(time.strftime("%d-%m-%Y"))