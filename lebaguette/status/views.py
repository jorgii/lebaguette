import psutil
from datetime import datetime
from subprocess import check_output, CalledProcessError, Popen, PIPE


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import Services


@login_required
def server_status(request):
    ram_usage = get_ram_usage()
    disk_data = get_disk_data()
    disk_usage = get_disk_usage()
    services_list = get_services_with_status()
    raid_data = get_raid_data()
    cpu_count = psutil.cpu_count()
    cpu_count_range = range(cpu_count)
    ps = Popen(['sensors'], stdout=PIPE)
    fans_count = len(check_output(["grep", "fan"], stdin=ps.stdout).decode("utf-8").split("\n")) - 1
    fans_count_range = range(fans_count)
    return render(request, 'status/status.html', locals())


def get_ram_usage():
    memory = psutil.virtual_memory()
    data = {}
    data['units'] = 'MB'
    data['total'] = round(memory.total/1048576, 2)
    data['used'] = round(memory.used/1048576, 2)
    data['available'] = round(memory.available/1048576, 2)
    data['percent'] = memory.percent
    return data


def get_disk_data():
    disk_partitions = psutil.disk_partitions()
    data = {}
    for partition in disk_partitions:
        data[partition.device] = {'device': partition.device,
                                  'mount_point': partition.mountpoint,
                                  'fstype': partition.fstype}
    return data


def get_raid_data():
    try:
        raid_data = check_output(["cat", "/proc/mdstat"]).decode("utf-8").split("\n")
    except CalledProcessError:
        raid_data = 'RAID data not found'
    return raid_data


def get_disk_usage():
    disk_partitions = psutil.disk_partitions()
    data = {}
    for partition in disk_partitions:
        data[partition.device] = {
         'units': 'GB',
         'total': round(psutil.disk_usage(partition.mountpoint).total/1073741824, 2),
         'used': round(psutil.disk_usage(partition.mountpoint).used/1073741824, 2),
         'free': round(psutil.disk_usage(partition.mountpoint).free/1073741824, 2),
         'percent': psutil.disk_usage(partition.mountpoint).percent}
    return data


def get_uptime():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    minutes, seconds = divmod(uptime.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    data = {}
    data['days'] = days
    data['hours'] = hours
    data['minutes'] = minutes
    data['seconds'] = seconds
    return data


def get_services_with_status():
    data = {}
    for service in Services.objects.all():
        service_status = get_service_status(str(service)).strip()
        if 'running' in service_status:
            data[str(service)] = [service_status, True]
        else:
            data[str(service)] = [service_status, False]
    return data


def get_service_status(servicename):
    try:
        service_data = Popen(["service", servicename, "status"], stdout=PIPE)
        service_data = check_output(["grep", "Active"], stdin=service_data.stdout).decode("utf-8")
        service_data = service_data.replace("\n", '')
    except CalledProcessError:
        service_data = 'Service not found'
    return service_data
