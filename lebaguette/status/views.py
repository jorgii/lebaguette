import psutil
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def server_status(request):
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    memory_usage = get_memory()
    disk_partitions = psutil.disk_partitions()
    disk_usage = psutil.disk_usage('/')
    network_connections = psutil.net_connections()
    net_if_address = psutil.net_if_addrs()
    users = psutil.users()
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    m, s = divmod(uptime.seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    processes = get_processes()

    return render(request, 'status/status.html', locals())

def get_memory():
    memory = psutil.virtual_memory()

    return {'Total memory':round(memory.total/1048576,2),'Used memory':round(memory.used/1048576,2), 'Percent usage': memory.percent}

def get_processes():
    pids = psutil.pids()
    pids_dict = {}

    for pid in pids:
        pids_dict[pid] = psutil.Process(pid).as_dict()
    
    return pids_dict            