from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def server_status(request):
    return render(request, 'status/status.html', locals())
