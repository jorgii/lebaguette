from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import permission_required


from .models import Request


@permission_required('requestmedia.view')
@login_required
def request_media(request):
    request_items = Request.objects.filter(status='N').order_by(
        '-datetime_requested')
    paginator = Paginator(request_items, 15)
    page = request.GET.get('page')
    try:
        request_items_page = paginator.page(page)
    except PageNotAnInteger:
        request_items_page = paginator.page(number=1)
    except EmptyPage:
        request_items_page = paginator.page(paginator.num_pages)
    return render(request, 'requestmedia/request_media.html', locals())


@permission_required('requestmedia.view')
@login_required
def approved_media(request):
    request_items = Request.objects.filter(status='A').order_by(
        '-datetime_approved')
    paginator = Paginator(request_items, 15)
    page = request.GET.get('page')
    try:
        request_items_page = paginator.page(page)
    except PageNotAnInteger:
        request_items_page = paginator.page(number=1)
    except EmptyPage:
        request_items_page = paginator.page(paginator.num_pages)
    return render(request, 'requestmedia/approved_media.html', locals())


@permission_required('requestmedia.view')
@login_required
def rejected_media(request):
    request_items = Request.objects.filter(status='R').order_by(
        '-datetime_rejected')
    paginator = Paginator(request_items, 15)
    page = request.GET.get('page')
    try:
        request_items_page = paginator.page(page)
    except PageNotAnInteger:
        request_items_page = paginator.page(number=1)
    except EmptyPage:
        request_items_page = paginator.page(paginator.num_pages)
    return render(request, 'requestmedia/rejected_media.html', locals())


@permission_required('requestmedia.view')
@login_required
def completed_media(request):
    request_items = Request.objects.filter(status='C').order_by(
        '-datetime_completed')
    paginator = Paginator(request_items, 15)
    page = request.GET.get('page')
    try:
        request_items_page = paginator.page(page)
    except PageNotAnInteger:
        request_items_page = paginator.page(number=1)
    except EmptyPage:
        request_items_page = paginator.page(paginator.num_pages)
    return render(request, 'requestmedia/completed_media.html', locals())
