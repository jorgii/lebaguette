from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Coalesce


from .models import Request
from lebaguette.extra import is_in_group


@login_required
def request_media(request):
    request_items = Request.objects.filter(status='N').order_by(
        '-datetime_requested')
#    paginator = Paginator(media_items, 5)
#    page = request.GET.get('page')
#    try:
#        media_items_page = paginator.page(page)
#    except PageNotAnInteger:
#        media_items_page = paginator.page(number=1)
#    except EmptyPage:
#        media_items_page = paginator.page(paginator.num_pages)
    return render(request, 'requestmedia/request_media.html', locals())
