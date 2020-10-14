import mock
import django.utils.timezone
from datetime import timedelta
from django import test

from api import models


class CreateAndListMovieTestCase(test.TestCase):
    @mock.patch('api.views.CreateAndListMovieView.get_omdb_api_body')
    def test_create_movie(self, mock_get_omdb_api_body):
        mock_get_omdb_api_body.return_value = {"Title":"Guardians of the Galaxy Vol. 2","Year":"2017","Rated":"PG-13","Released":"05 May 2017","Runtime":"136 min","Genre":"Action, Adventure, Comedy, Sci-Fi","Director":"James Gunn","Writer":"James Gunn, Dan Abnett (based on the Marvel comics by), Andy Lanning (based on the Marvel comics by), Steve Englehart (Star-Lord created by), Steve Gan (Star-Lord created by), Jim Starlin (Gamora and Drax created by), Stan Lee (Groot created by), Larry Lieber (Groot created by), Jack Kirby (Groot created by), Bill Mantlo (Rocket Raccoon created by), Keith Giffen (Rocket Raccoon created by), Steve Gerber (Howard the Duck created by), Val Mayerik (Howard the Duck created by)","Actors":"Chris Pratt, Zoe Saldana, Dave Bautista, Vin Diesel","Plot":"The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father the ambitious celestial being Ego.","Language":"English","Country":"USA","Awards":"Nominated for 1 Oscar. Another 15 wins & 56 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BNjM0NTc0NzItM2FlYS00YzEwLWE0YmUtNTA2ZWIzODc2OTgxXkEyXkFqcGdeQXVyNTgwNzIyNzg@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.6/10"},{"Source":"Rotten Tomatoes","Value":"85%"},{"Source":"Metacritic","Value":"67/100"}],"Metascore":"67","imdbRating":"7.6","imdbVotes":"552,519","imdbID":"tt3896198","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"Marvel Studios, Walt Disney Pictures","Website":"N/A","Response":"True"}  # noqa
        response = self.client.post('/movies/',
                                    data={'title': 'Guardians of the Galaxy Vol. 2'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

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


class DeleteAndUpdateMovieTestCase(test.TestCase):
    def test_delete(self):
        movie = models.Movie(title='Song of Water and Mud',
                             year='2020',
                             runtime='136 min',
                             genre='Fantasy',
                             external_api_response={})
        movie.save()
        response = self.client.delete('/movies/{}/'.format(movie.pk))
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        movie = models.Movie(title='Song of Water and Mud',
                             year='2020',
                             runtime='136 min',
                             genre='Fantasy',
                             external_api_response={})
        movie.save()
        response = self.client.put('/movies/{}/'.format(movie.pk),
                                   data={'title': 'Song of Ice and Mud',
                                         'year': '2021',
                                         'runtime': '133 min',
                                         'genre': 'Science Fiction'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        movie = models.Movie.objects.get(pk=movie.pk)
        self.assertEqual(movie.to_json(),
                         {'title': 'Song of Ice and Mud',
                          'year': '2021',
                          'runtime': '133 min',
                          'genre': 'Science Fiction',
                          'external_api_response': {}})


class CreateAndListCommentTestCase(test.TestCase):
    def test_create(self):
        movie = models.Movie(title='Song of Water and Mud',
                             year='2020',
                             runtime='136 min',
                             genre='Fantasy',
                             external_api_response={})
        movie.save()

        response = self.client.post('/comments/',
                                    data={'movie': movie.pk,
                                          'text_body': 'My first comment ever.'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_movie_not_found(self):
        response = self.client.post('/comments/',
                                    data={'movie': 1000,
                                          'text_body': 'My first comment ever.'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_list(self):
        first_movie = models.Movie(title='Song of Water and Mud',
                                   year='2020',
                                   runtime='136 min',
                                   genre='Fantasy',
                                   external_api_response={})
        first_movie.save()
        second_movie = models.Movie(title='Song of Ice and Fire',
                                    year='2020',
                                    runtime='136 min',
                                    genre='Fantasy',
                                    external_api_response={})
        second_movie.save()

        comment = models.Comment(movie=first_movie, text_body='It is my first comment.')
        comment.save()
        comment = models.Comment(movie=first_movie, text_body='It is my second comment.')
        comment.save()
        comment = models.Comment(movie=second_movie, text_body='It is my third comment.')
        comment.save()

        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['comments']), 3)

        response = self.client.get('/comments/?movie_pk={}'.format(second_movie.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['comments']), 1)


class TopTestCase(test.TestCase):
    def test_top(self):
        first_movie = models.Movie(title='Song of Water and Mud 1',
                                   year='2020',
                                   runtime='136 min',
                                   genre='Fantasy',
                                   external_api_response={})
        first_movie.save()
        comment = models.Comment(movie=first_movie, text_body='1')
        comment.save()
        comment = models.Comment(movie=first_movie, text_body='1')
        comment.save()
        second_movie = models.Movie(title='Song of Water and Mud 2',
                                    year='2020',
                                    runtime='136 min',
                                    genre='Fantasy',
                                    external_api_response={})
        second_movie.save()
        comment = models.Comment(movie=second_movie, text_body='1')
        comment.save()
        third_movie = models.Movie(title='Song of Water and Mud 3',
                                   year='2020',
                                   runtime='136 min',
                                   genre='Fantasy',
                                   external_api_response={})
        third_movie.save()
        comment = models.Comment(movie=third_movie, text_body='1')
        comment.save()
        fourth_movie = models.Movie(title='Song of Water and Mud 4',
                                    year='2020',
                                    runtime='136 min',
                                    genre='Fantasy',
                                    external_api_response={})
        fourth_movie.save()

        now = django.utils.timezone.now()
        day_ago = now - timedelta(days=1)
        start = day_ago.timestamp()
        end = now.timestamp()
        response = self.client.get('/top/?start={}&end={}'.format(start, end))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(),
                             [{'movie_id': first_movie.pk, 'rank': 1, 'total_comments': 2},
                              {'movie_id': second_movie.pk, 'rank': 2, 'total_comments': 1},
                              {'movie_id': third_movie.pk, 'rank': 2, 'total_comments': 1}])
