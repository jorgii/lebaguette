from django.db import models


class MediaItem(models.Model):
    MEDIA_TYPES = (
        ('MV', 'Movie'),
        ('TV', 'TV Show')
    )
    title = models.CharField('Title',
                             max_length=255,
                             blank=False,
                             null=False)
    type = models.CharField(max_length=2, choices=MEDIA_TYPES)
    released = models.DateField()
    imdb_rating = models.DecimalField(decimal_places=1, max_digits=2)
    imdb_id = models.CharField('IMDB ID',
                               max_length=255,
                               blank=False,
                               null=False)
    completed = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
