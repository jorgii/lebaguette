import re

from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Request, MediaItem


@permission_required('requestmedia.add_request')
@login_required
def add_request(request):
    if request.is_ajax() and request.method == 'POST':
        pattern = r'tt\d+'
        to_parse = request.POST.get('imdb_id')
        try:
            imdbid_list = re.findall(pattern, to_parse)
            for imdb_id in imdbid_list:
                media_item = MediaItem.create_media_from_imdbid(imdb_id)
                media_item.save_and_create_request(request.user, 'N')
        except:
            raise Http404
        return HttpResponse(
            '"' +
            str(media_item) +
            '" added')
    else:
        return HttpResponseForbidden()


@permission_required('requestmedia.complete')
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
            str(request_item.media_item) +
            '" marked as completed')
    else:
        return HttpResponseForbidden()


@permission_required('requestmedia.approve')
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
            str(request_item.media_item) +
            '" marked as approved')
    else:
        return HttpResponseForbidden()


@permission_required('requestmedia.reject')
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
            str(request_item.media_item) +
            '" marked as rejected')
    else:
        return HttpResponseForbidden()
