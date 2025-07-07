from django.db import models


class DailyNote(models.Model):

    title = models.CharField(max_length=100)
