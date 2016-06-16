from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Request
from lebaguette.extra import is_in_group


@is_in_group
@login_required
def mark_request_complete(request):
    if request.is_ajax() and request.method == 'POST':
        itemid = request.POST.get('itemid')
        try:
            request_item = Request.objects.get(id=itemid)
            request_item.mark_as_complete(request.user)
        except:
            raise Http404
        return HttpResponse(
            '"' +
            str(request_item.get_media_item()) +
            '" marked as complete')
    else:
        return HttpResponseForbidden()
