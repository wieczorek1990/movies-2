import mock
from django import test

from api import models


class CreateAndListMovieTestCase(test.TestCase):
    @mock.patch('api.views.CreateAndListMovieView.get_omdb_api_body')
    def test_create_movie(self, mock_get_omdb_api_body):
        mock_get_omdb_api_body.return_value = {"Title":"Guardians of the Galaxy Vol. 2","Year":"2017","Rated":"PG-13","Released":"05 May 2017","Runtime":"136 min","Genre":"Action, Adventure, Comedy, Sci-Fi","Director":"James Gunn","Writer":"James Gunn, Dan Abnett (based on the Marvel comics by), Andy Lanning (based on the Marvel comics by), Steve Englehart (Star-Lord created by), Steve Gan (Star-Lord created by), Jim Starlin (Gamora and Drax created by), Stan Lee (Groot created by), Larry Lieber (Groot created by), Jack Kirby (Groot created by), Bill Mantlo (Rocket Raccoon created by), Keith Giffen (Rocket Raccoon created by), Steve Gerber (Howard the Duck created by), Val Mayerik (Howard the Duck created by)","Actors":"Chris Pratt, Zoe Saldana, Dave Bautista, Vin Diesel","Plot":"The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father the ambitious celestial being Ego.","Language":"English","Country":"USA","Awards":"Nominated for 1 Oscar. Another 15 wins & 56 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjM0NTc0NzItM2FlYS00YzEwLWE0YmUtNTA2ZWIzODc2OTgxXkEyXkFqcGdeQXVyNTgwNzIyNzg@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.6/10"},{"Source":"Rotten Tomatoes","Value":"85%"},{"Source":"Metacritic","Value":"67/100"}],"Metascore":"67","imdbRating":"7.6","imdbVotes":"552,519","imdbID":"tt3896198","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"Marvel Studios, Walt Disney Pictures","Website":"N/A","Response":"True"}  # noqa
        response = self.client.post('/movies/',
                                    data={'title': 'Guardians of the Galaxy Vol. 2'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_list_movies(self):
        movie = models.Movie(title='Song of Water and Mud',
                             year='2020',
                             runtime='136 min',
                             genre='Fantasy',
                             external_api_response={})
        movie.save()
        movie = models.Movie(title='Song of Ice and Fire',
                             year='2020',
                             runtime='136 min',
                             genre='Fantasy',
                             external_api_response={})
        movie.save()

        response = self.client.get('/movies/')
        self.assertEqual(response.json()['movies'],
                         [
                             {
                                 'title': 'Song of Ice and Fire',
                                 'year': '2020',
                                 'runtime': '136 min',
                                 'genre': 'Fantasy',
                                 'external_api_response': {}
                             },
                             {
                                 'title': 'Song of Water and Mud',
                                 'year': '2020',
                                 'runtime': '136 min',
                                 'genre': 'Fantasy',
                                 'external_api_response': {}
                             },
                         ])