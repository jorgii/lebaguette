from datetime import datetime, date

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
    poster_link = models.CharField(
        'Poster Link',
        max_length=255,
        blank=True,
        null=True)
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
    season_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('tv_show', 'season_number')

    def __str__(self):
        return (self.tv_show.title + ': Season ' + str(self.season_number))

    @classmethod
    def create(cls, tv_show, season_number):
        return cls(tv_show=tv_show, season_number=season_number)

    def create_episodes_from_json(self, episodes_json):
        for episode in episodes_json['Episodes']:
            # create non existent episodes that have already aired
            try:
                if not TVShowEpisode.objects.filter(
                            episode_number=int(episode['Episode']),
                            season=self,
                            episode_imdbid=episode['imdbID']).exists() and \
                        date.today() >= datetime.strptime(
                            episode['Released'],
                            '%Y-%m-%d').date():
                    tv_show_episode = TVShowEpisode.create(
                        season=self,
                        episode_title=episode['Title'],
                        episode_number=int(episode['Episode']),
                        episode_released=datetime.strptime(
                            episode['Released'],
                            '%Y-%m-%d').date(),
                        episode_imdbid=episode['imdbID'])
                    tv_show_episode.save()
            except ValueError:
                continue


class TVShowEpisode(models.Model):
    season = models.ForeignKey(TVShowSeason, on_delete=models.CASCADE)
    episode_title = models.CharField('Episode Title',
                                     max_length=255,
                                     blank=False,
                                     null=False)
    episode_number = models.IntegerField()
    episode_released = models.DateField()
    episode_imdbid = models.CharField(
        'Episode IMDB ID',
        max_length=255,
        blank=False,
        null=False)
    episode_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('season', 'episode_number')

    def mark_as_complete(self):
        self.episode_completed = True
        self.save()

    def __str__(self):
        return (
            self.season.tv_show.title +
            ': S' + str(self.season.season_number) +
            'E' + str(self.episode_number))

    @classmethod
    def create(
            cls,
            season,
            episode_title,
            episode_number,
            episode_released,
            episode_imdbid):
        return cls(
            season=season,
            episode_title=episode_title,
            episode_number=episode_number,
            episode_released=episode_released,
            episode_imdbid=episode_imdbid)


class Movie(MediaItem):
    def __str__(self):
        return self.title
