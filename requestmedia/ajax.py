import re
import logging

from django.http import HttpResponseForbidden, HttpResponse,\
    HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Request, MediaItem

logger = logging.getLogger('django.error')


@permission_required('requestmedia.add_request')
@login_required
def add_request(request):
    if request.is_ajax() and request.method == 'POST':
        pattern = r'tt\d+'
        to_parse = request.POST.get('imdb_id')
        try:
            imdbid_list_not_added = []
            imdbid_list = re.findall(pattern, to_parse)
            if not imdbid_list:
                return HttpResponseBadRequest(reason='IMDB ID not found!')
            for imdb_id in imdbid_list:
                if MediaItem.objects.filter(imdb_id=imdb_id).exists():
                    imdbid_list_not_added.append(imdb_id)
                    continue
                media_item = MediaItem.create_media_from_imdbid(imdb_id)
                media_item.save_and_create_request(request.user, 'N')
            if imdbid_list_not_added and \
                    len(imdbid_list) == len(imdbid_list_not_added):
                return HttpResponseBadRequest(
                    reason='All itmes already exist in the database')
            elif imdbid_list_not_added and \
                    len(imdbid_list) != len(imdbid_list_not_added):
                message = 'Items ' + str(imdbid_list_not_added) + \
                    ' already exist. The rest were added!'
                return HttpResponseBadRequest(reason=message)
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest(reason=e)
        else:
            return HttpResponse(
                '"' +
                str(media_item) +
                '" added')
        return HttpResponse('IMDB ID not found!')
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
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest(reason=e)
        else:
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
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest(reason=e)
        else:
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
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest(reason=e)
        else:
            return HttpResponse(
                '"' +
                str(request_item.media_item) +
                '" marked as rejected')
    else:
        return HttpResponseForbidden()
