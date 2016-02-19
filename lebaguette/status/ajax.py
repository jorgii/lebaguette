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

def get_disk_data(request):
    if request.is_ajax():
        disk_partitions = psutil.disk_partitions()
        data = {}
        for partition in disk_partitions:
            data['partition'] = {'device':partition.device, 'mount_point':partition.mountpoint, 'fstype':partition.fstype}

        data = json.dumps(data)
        return HttpResponse(data,content_type='application/json')
    else:
        raise Http404

def get_disk_usage(request):
    if request.is_ajax():
        disk_partitions = psutil.disk_partitions()
        data = {}
        for partition in disk_partitions:
            data['disk'] = {'device':partition.device,
                                     'total':round(psutil.disk_usage(partition.mountpoint).total/1073741824,2),
                                     'used':round(psutil.disk_usage(partition.mountpoint).used/1073741824,2),
                                     'free':round(psutil.disk_usage(partition.mountpoint).free/1073741824,2),
                                     'percent':psutil.disk_usage(partition.mountpoint).percent
                                    }
        data = json.dumps(data)
        return HttpResponse(data,content_type='application/json')
    else:
        raise Http404
