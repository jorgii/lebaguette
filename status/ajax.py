import psutil
import platform
from subprocess import check_output, Popen, PIPE


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
            ps = Popen(['sensors'], stdout=PIPE)
            temps = check_output(
                ["grep", "Core"],
                stdin=ps.stdout).decode("utf-8")
            data = {}
            for temp in temps.split("\n"):
                if temp != '':
                    data[temp.split(":")[0]] = temp.split(":")[1].strip()[
                        1:5].strip()
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


@permission_required('status.view')
@login_required
def get_fanspeed(request):
    if request.is_ajax():
        if 'Linux' in platform.platform():
            ps = Popen(['sensors'], stdout=PIPE)
            fans = check_output(
                ["grep", "fan"],
                stdin=ps.stdout).decode("utf-8")
            data = {}
            for fan in fans.split("\n"):
                if fan != '':
                    if fan.split(":")[1].strip()[:5] != "0 RPM":
                        data[fan.split(":")[0]] = \
                            fan.split(":")[1].strip()[:4].strip()
            data = json.dumps(data)
            return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
