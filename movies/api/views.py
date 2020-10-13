import requests
from django.conf import settings
from rest_framework import exceptions
from rest_framework import response
from rest_framework import views
from api import models
from api import serializers


class ExternalAPIException(exceptions.APIException):
    pass


class CreateAndListMovieView(views.APIView):
    @staticmethod
    def get_omdb_api_body(title):
        response = requests.get('http://www.omdbapi.com/?apikey={}&t={}'.format(
            settings.OMDB_API_KEY, title))
        if response.status_code == 200:
            return response.json()
        else:
            raise ExternalAPIException()

    @classmethod
    def post(cls, request):
        serializer = serializers.CreateMovieSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(status=400)
        title = serializer.validated_data['title']

        body = cls.get_omdb_api_body(title)
        body = {key.lower(): value for key, value in body.items()}

        try:
            movie = models.Movie.objects.get(title=body['title'])
        except models.Movie.DoesNotExist:
            movie = models.Movie(title=body['title'],
                                 year=body['year'],
                                 runtime=body['runtime'],
                                 genre=body['genre'],
                                 external_api_response=body)
            movie.save()

        return response.Response(status=200, data={
            'movie': movie.to_json(),
            'external_api_response': body,
        })

    @staticmethod
    def get(request):
        movies = models.Movie.objects.all().order_by('title')
        return response.Response(status=200,
                                 data={'movies': [movie.to_json() for movie in movies]})
