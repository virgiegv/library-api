from django.db import models
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    title = models.CharField(
        blank=True,
        null=True,
    )


class Author(models.Model):
    name = models.CharField(
        blank=True,
        null=True,
    )


class Book(models.Model):
    title = models.CharField(
        max_length=500,
        blank=False,
        null=False,
    )

    subtitle = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    authors = models.ManyToManyField(Author, blank=True)

    categories = models.ManyToManyField(Category, blank=True)

    published_date = models.CharField(
        max_length=300,
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

    image = models.URLField(
        max_length=1000,
        blank=True,
        null=True)

    original_source = models.CharField(
        null=True,
        blank=True,
    )

    original_source_id = models.CharField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['original_source', 'original_source_id'],
                name='source constraint'
            )
        ]

