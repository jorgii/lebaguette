from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import TVShowEpisode


@login_required
def mark_episode_complete(request):
    if request.is_ajax() and request.method == 'POST':
        imdbid = request.POST.get('imdbid')
        try:
            episode = TVShowEpisode.objects.get(episode_imdbid=imdbid)
            episode.mark_as_complete()
        except:
            raise Http404
        return HttpResponse('"' + str(episode) + '" marked as complete')
    else:
        return HttpResponseForbidden()
