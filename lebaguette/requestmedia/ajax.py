import re

from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Request


#@permission_required('requestmedia.add_request')
#@login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_request(request):
#    if request.is_ajax() and request.method == 'POST':
        pattern = r'tt\d+'
        imdbid_list = re.findall(pattern, request.POST.get('imdbid'))
        #try:
        print(imdbid_list)
        for imdbid in imdbid_list:
            media_request = Request.create(imdbid, request.user)
            media_request.save()
        #except:
        #    raise Http404
        #return HttpResponse(
        #    '"' +
            #str(media_request.get_media_item()) +
        #    '" added')
#    else:
#        return HttpResponseForbidden()


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
            str(request_item.get_media_item()) +
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
            str(request_item.get_media_item()) +
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
            str(request_item.get_media_item()) +
            '" marked as rejected')
    else:
        return HttpResponseForbidden()
