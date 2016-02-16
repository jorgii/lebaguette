import psutil

from django.shortcuts import render

def server_status(request):
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    memory_usage = psutil.virtual_memory()
    disk_partitions = psutil.disk_partitions()
    disk_usage = psutil.disk_usage('/')
    return render(request, 'status/status.html', locals())