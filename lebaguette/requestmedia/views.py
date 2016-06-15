from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Coalesce


from .models import TVShowEpisode
from lebaguette.extra import is_in_group


@login_required
def request_media(request):
    media_items = TVShowEpisode.objects.all().order_by(
        Coalesce('episode_released', 'episode_title').desc())
    paginator = Paginator(media_items, 5)
    page = request.GET.get('page')
    try:
        media_items_page = paginator.page(page)
    except PageNotAnInteger:
        media_items_page = paginator.page(number=1)
    except EmptyPage:
        media_items_page = paginator.page(paginator.num_pages)
    return render(request, 'requestmedia/request_media.html', locals())


@is_in_group
@login_required
def episodes(request):
    episodes = TVShowEpisode.objects.filter(
        episode_completed=False,
        season__tv_show__show_completed=False,
        season__season_completed=False).order_by(
        Coalesce('episode_released', 'episode_title').desc())
    return render(request, 'requestmedia/episodes.html', locals())
