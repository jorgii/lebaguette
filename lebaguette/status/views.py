import psutil
from datetime import datetime
from subprocess import check_output, CalledProcessError


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def server_status(request):
    ram_usage = get_ram_usage()
    disk_data = get_disk_data()
    disk_usage = get_disk_usage()
    plex_status = get_service('plexmediaserver')
    transmission_status = get_service('transmission-daemon')
    apache2_status = get_service('apache2')
    raid_data = get_raid_data()
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
    data = {}
    try:
        data['raid_data'] = check_output(["cat", "/proc/mdstat"]).decode("utf-8")
    except CalledProcessError:
        data['raid_data'] = 'Service not found'
    return data


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


def get_service(servicename):
    data = {}
    try:
        service_data = check_output(["service", servicename, "status"]).decode("utf-8")
        data[servicename] = service_data.replace("\n", "<br>")
    except CalledProcessError:
        data[servicename] = 'Service not found'
    return data
