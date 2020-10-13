from django.db import models


class Movie(models.Model):
    title = models.TextField()
    year = models.TextField()
    runtime = models.TextField()
    genre = models.TextField()
    external_api_response = models.JSONField()

    def to_json(self):
        return {
            'title': self.title,
            'year': self.year,
            'runtime': self.runtime,
            'genre': self.genre,
            'external_api_response': self.external_api_response,
        }
