from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Book(models.Model):
    title = models.CharField(
        max_length=300,
        blank=False,
        null=False,
    )

    subtitle = models.CharField(
        max_length=300,
        blank=False,
        null=False,
    )

    authors = ArrayField(
        models.CharField(
            null=False,
            blank=False
        ),
        null=False,
        blank=False,
    )

    categories = ArrayField(
        models.CharField(
            null=False,
            blank=False
        ),
        null=False,
        blank=False,
    )

    published_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )

    editor = models.CharField(
        max_length=300,
        blank=False,
        null=False,
    )

    description = models.TextField(
        blank=True,
        null=False,
    )

    image = models.URLField(blank=True, null=True)
