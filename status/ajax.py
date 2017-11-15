import psutil
import platform


import json
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


@permission_required('status.view')
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


@permission_required('status.view')
@login_required
def get_temperatures(request):
    if request.is_ajax():
        if 'Linux' in platform.platform():
            core_temps = psutil.sensors_temperatures()['coretemp']
            data = {}
            for temp in core_temps:
                data[temp.label] = temp.current
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


@permission_required('status.view')
@login_required
def get_fanspeed(request):
    if request.is_ajax():
        if 'Linux' in platform.platform():
            data = {}
            for fans_list in psutil.sensors_fans().values():
                for index, fan in enumerate(fans_list):
                    if fan.current > 0:
                        data['Fan {}'.format(index)] = fan.current
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
