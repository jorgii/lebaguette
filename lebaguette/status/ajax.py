import psutil
from datetime import datetime


import json
from django.http import Http404, HttpResponse



def get_cpu_usage(request):
    if request.is_ajax():
        cpu_count = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent(percpu=True)
        data = {}
        data['cpu_count'] = cpu_count
        data['cpu_usage'] = cpu_usage
        data = json.dumps(data)
        return HttpResponse(data,content_type='application/json')
    else:
        raise Http404


def get_ram_usage(request):
    if request.is_ajax():
        memory = psutil.virtual_memory()
        data = {}
        data['units'] = 'MB'
        data['total'] = round(memory.total/1048576,2)
        data['used'] = round(memory.used/1048576,2)
        data['available'] = round(memory.available/1048576,2)
        data['percent'] = memory.percent
        data = json.dumps(data)
        return HttpResponse(data,content_type='application/json')
    else:
        raise Http404    
