from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Request
from lebaguette.extra import is_in_group


@is_in_group
@login_required
def complete_request(request):
    if request.is_ajax() and request.method == 'POST':
        itemid = request.POST.get('itemid')
        try:
            request_item = Request.objects.get(id=itemid)
            request_item.complete(request.user)
        except:
            raise Http404
        return HttpResponse(
            '"' +
            str(request_item.get_media_item()) +
            '" marked as completed')
    else:
        return HttpResponseForbidden()


@is_in_group
@login_required
def approve_request(request):
    if request.is_ajax() and request.method == 'POST':
        itemid = request.POST.get('itemid')
        try:
            request_item = Request.objects.get(id=itemid)
            request_item.approve(request.user)
        except:
            raise Http404
        return HttpResponse(
            '"' +
            str(request_item.get_media_item()) +
            '" marked as approved')
    else:
        return HttpResponseForbidden()


@is_in_group
@login_required
def reject_request(request):
    if request.is_ajax() and request.method == 'POST':
        itemid = request.POST.get('itemid')
        try:
            request_item = Request.objects.get(id=itemid)
            request_item.reject(request.user)
        except:
            raise Http404
        return HttpResponse(
            '"' +
            str(request_item.get_media_item()) +
            '" marked as rejected')
    else:
        return HttpResponseForbidden()
