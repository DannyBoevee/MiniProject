import requests
import time
import xmltodict

class Api:
    api_key = None
    api_web = None

    def __init__(self):
        self.api_key = '9smtwozmiugid4m8m5f9n6g1oaiwt6r4'
        self.api_web = 'http://www.filmtotaal.nl/api/filmsoptv.xml'

    def getApiUrl(self, date, sort):
        return "{0}?apikey={1}&dag={2}&sorteer={3}" . format(self.api_web, self.api_key, date, sort)

    def getApiData(self, date, sort):
        """
        Data op halen uit de Filmtotaal Api
        :param date: String
            Invoer ("Dag - Maand - Jaar")
        :param sort: String
            0 = Alle films
            1 = filmtips
            2 = film van de dag
        :return:
            Wanneer de data opgehaald kan worden:
                Dictionary
            Wanneer er iets mis is gegaan:
                False
        """
        try:
            request = requests.get(self.getApiUrl(date, sort))
            data = xmltodict.parse(request.text)
        except:
            return False
        finally:
            return data['filmsoptv']['film']

    def getCurrentTime(self):
        """
            Krijg huidige datum
        :return:
            (String) Dag - Maand - Jaar
        """
        return time.strftime(time.strftime("%d-%m-%Y"))

    def getMovieList(self, date):
        """
        Het verkrijgen van alle films op de gekozen dag.
        :param date:
            (String) Dag - Maand - Jaar
        :return:
            (List) Alle titels
        """
        data = self.getApiData(date, "0")
        movies = []
        for movie in data:
            movies.append(movie['titel'])
        return movies

    def getDailyrRecommendable(self, date):
        """
        Het verkrijgen van alle films op de gekozen dag.
        :param date:
            (String) Dag - Maand - Jaar
        :return:
            (String) met de tip van de dag
        """
        data = self.getApiData(date, "2")
        return data['titel']

    def getMovieDescription(self, movieTitle, date):
        """
            Het verkrijgen van de film beschrijving
        :param movieTitle:
            (String) De titel van de film
        :param date:
            (String) Dag - Maand - Jaar
        :return:
            Wanneer de film is gevonden:
                (Dictonairy):
                    ft_link
                    titel
                    jaar
                    regisseur
                    cast
                    genre
                    land
                    cover
                    tagline
                    duur
                    synopsis
                    ft_rating
                    ft_votes
                    imdb_id
                    imdb_rating
                    imdb_votes
                    starttijd
                    eindtijd
                    zender
                    filmtip
            Zodra de film niet is gevonden:
                (Boolean) False
            """
        data = self.getApiData(date, "0")
        for movie in data:
            if (movie['titel'] == movieTitle):
                return movie
            else:
                return False
