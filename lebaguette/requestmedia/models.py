from django.db import models


class MediaItem(models.Model):
    title = models.CharField('Title',
                             max_length=255,
                             blank=False,
                             null=False)
    released = models.DateField()
    imdb_rating = models.DecimalField(decimal_places=1, max_digits=2)
    imdb_id = models.CharField('IMDB ID',
                               max_length=255,
                               blank=False,
                               null=False)
    request_completed = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta():
        abstract = True

    def __str__(self):
        return self.title


class TVShow(MediaItem):
    show_completed = models.BooleanField(default=False)


class TVShowSeason(models.Model):
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    season_number = models.IntegerField()

    class Meta:
        unique_together = ('tv_show', 'season_number')

    def __str__(self):
        return (self.tv_show.title + ': Season ' + str(self.season_number))

    @classmethod
    def create(cls, tv_show, season_number):
        return cls(tv_show=tv_show, season_number=season_number)


class TVShowEpisode(models.Model):
    season = models.ForeignKey(TVShowSeason, on_delete=models.CASCADE)
    episode_title = models.CharField('Episode Title',
                                     max_length=255,
                                     blank=False,
                                     null=False)
    episode_number = models.IntegerField()
    episode_imdbid = models.CharField(
        'Episode IMDB ID',
        max_length=255,
        blank=False,
        null=False)

    class Meta:
        unique_together = ('season', 'episode_number')

    def __str__(self):
        return (
            self.season.tv_show.title +
            ': S' + str(self.season.season_number) +
            'E' + str(self.episode_number))

    @classmethod
    def create(cls, season, episode_title, episode_number):
        return cls(season=season,
                   episode_title=episode_title,
                   episode_number=episode_number)


class Movie(MediaItem):
    def __str__(self):
        return self.title
