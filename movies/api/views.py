import datetime
import requests
from django.conf import settings
from rest_framework import exceptions
from rest_framework import response
from rest_framework import views
from rest_framework import viewsets
from rest_framework import mixins

from api import helpers
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
            status = 200
        except models.Movie.DoesNotExist:
            movie = models.Movie(title=body['title'],
                                 year=body['year'],
                                 runtime=body['runtime'],
                                 genre=body['genre'],
                                 external_api_response=body)
            movie.save()
            status = 201

        return response.Response(status=status, data={
            'movie': movie.to_json(),
            'external_api_response': body,
        })

    @staticmethod
    def get(request):
        movies = models.Movie.objects.all().order_by('title')
        return response.Response(status=200,
                                 data={'movies': [movie.to_json() for movie in movies]})


class DeleteAndUpdateModelViewSet(mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer


class CreateAndListCommentView(views.APIView):
    @staticmethod
    def post(request):
        serializer = serializers.CreateCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(status=400)

        comment = models.Comment(movie=serializer.validated_data['movie'],
                                 text_body=serializer.validated_data['text_body'])
        comment.save()

        return response.Response(status=200, data={'comment': comment.to_json()})

    @staticmethod
    def get(request):
        movie_pk = request.query_params.get('movie_pk', None)
        if movie_pk is None:
            comments = models.Comment.objects.all()
        else:
            if not helpers.is_int(movie_pk):
                return response.Response(status=400)
            comments = models.Comment.objects.filter(movie=int(movie_pk))
        return response.Response(status=200,
                                 data={'comments': [comment.to_json() for comment in comments]})


class TopView(views.APIView):
    def get(self, request):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        if start is None or end is None:
            return response.Response(status=400)
        if not helpers.is_float(start) or not helpers.is_float(end):
            return response.Response(status=400)
        start = datetime.datetime.fromtimestamp(float(start))
        end = datetime.datetime.fromtimestamp(float(end))

        data = {}
        comments = models.Comment.objects.filter(created_at__gte=start, created_at__lte=end)
        movie_pks = comments.values_list('movie__pk', flat=True)
        movies = models.Movie.objects.filter(pk__in=movie_pks)
        for movie in movies:
            data[movie.pk] = 0
        for comment in comments:
            data[comment.movie.pk] += 1
        ranking = []
        for movie_id, total_comments in data.items():
            ranking.append({'movie_id': movie_id, 'total_comments': total_comments})
        ranking = sorted(ranking, key=lambda k: -k['total_comments'])
        rank = 1
        for index in range(len(ranking)):
            if index == len(ranking) - 1:
                next = None
            else:
                next = ranking[index + 1]
            current = ranking[index]
            current['rank'] = rank
            if next is not None and next['total_comments'] != current['total_comments']:
                rank += 1
        return response.Response(status=200, data=ranking)
