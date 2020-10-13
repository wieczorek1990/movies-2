from rest_framework import serializers


class CreateMovieSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False)
