from django.contrib import admin

from .models import TVShow, TVShowSeason, TVShowEpisode, Movie, Request

admin.site.register(TVShow)
admin.site.register(TVShowSeason)
admin.site.register(TVShowEpisode)
admin.site.register(Movie)
admin.site.register(Request)
