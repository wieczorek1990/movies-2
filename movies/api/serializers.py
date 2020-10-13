from rest_framework import serializers

from api import models


class CreateMovieSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ('title', 'year', 'runtime', 'genre')
