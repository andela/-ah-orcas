# this is how the db will be structured.

from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

'''Django-autoslug is a reusable Django library
that provides an improved slug field which can automatically:
populate itself from another field and preserve
 uniqueness of the value'''
from autoslug import AutoSlugField
from versatileimagefield.fields import VersatileImageField


class Article(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='author',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    # creates a random identifier for a particular article from the title
    # field.
    slug = AutoSlugField(
        populate_from='title',
        blank=True,
        null=True,
        unique=True)
    title = models.CharField(
        _('Article field', 'title'),
        unique=True,
        max_length=128
    )
    description = models.TextField(
        _('Article Field', 'description'),
        blank=True,
        null=True
    )
    body = models.TextField(
        _('Article Field', 'body'),
        blank=True,
        null=True
    )
    image = VersatileImageField(
        'Image',
        upload_to='article/',
        width_field='width',
        height_field='height',
        blank=True,
        null=True
    )
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        _('Article field', 'created at'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _('Article field', 'updated at'),
        auto_now=True
    )

    class Meta:
        app_label = "article"

    def __str__(self):
        return self.title


class RateArticle(models.Model):
    """
    This is the article class. It holds data for the article.
    """
    rater = models.ForeignKey(
        "authentication.User",
        related_name="ratearticle",
        on_delete=models.CASCADE)  # link with the user who rated
    article = models.ForeignKey(
        "article.Article",
        related_name="ratearticle",
        on_delete=models.CASCADE)  # link with the article being rated
    rate = models.IntegerField(null=False, blank=False,
                               validators=[
                                   MaxValueValidator(5),
                                   MinValueValidator(1)
                               ])  # rate value column

    def __str__(self):
        """
        Return a human readable format
        """
        return self.rate