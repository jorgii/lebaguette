from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Request


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
