import psutil
from subprocess import check_output, CalledProcessError


import json
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def get_cpu_usage(request):
    if request.is_ajax():
        cpu_count = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent(percpu=True)
        data = {}
        data['cpu_count'] = cpu_count
        data['cpu_usage'] = cpu_usage
        data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

