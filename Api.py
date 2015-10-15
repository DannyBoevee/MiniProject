import time
import os
import requests
import xmltodict


class Api:
    api_key = None
    api_web = None

    def __init__(self):
        self.api_key = '9smtwozmiugid4m8m5f9n6g1oaiwt6r4'
        self.api_web = 'http://www.filmtotaal.nl/api/filmsoptv.xml'

    def getApiUrl(self, date, sort):
        """
            Verkrijgen van de Api Url
        :param date:
            (String) Dag - Maand - Jaar
        :param sort:
            0 = Alle films
            1 = filmtips
            2 = film van de dag
        :return:
        """
        return "{0}?apikey={1}&dag={2}&sorteer={3}".format(self.api_web, self.api_key, date, sort)

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

    def getMovieImage(self, url):
        data = requests.get(url).content
        data = str(data)
        line = data.split('<div id="film_cover"')
        imageUrl = line[1][17:45]
        if not os.path.exists('images/'):
            os.makedirs('images/')
        with open('images/' + imageUrl[14:-4] + '.jpg', 'wb') as file:
            file.write(requests.get("http://www.filmtotaal.nl/" + imageUrl).content)

        return 'images/' + imageUrl[14:]

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
            image = self.getMovieImage(movie['ft_link'])
            movies.append({"titel": movie['titel'], "starttijd": movie['starttijd'], "image": image})
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
            if movie['titel'] == movieTitle:
                return movie

        return False
