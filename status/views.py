import logging
import psutil
from datetime import datetime
from subprocess import check_output, CalledProcessError, Popen, PIPE
import platform


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


from .models import Services

logger = logging.getLogger('django.info')


@login_required
@permission_required('status.view')
def server_status(request):
    ram_usage = get_ram_usage()
    disk_usage = get_disk_usage()
    cpu_logical_count = psutil.cpu_count()
    cpu_physical_count = psutil.cpu_count(logical=False)
    cpu_logical_count_range = range(cpu_logical_count)
    cpu_physical_count_range = range(cpu_physical_count)
    cpu_thermal_sensors = psutil.sensors_temperatures()['coretemp']
    uptime = get_uptime()

    # Get linux specific data
    if 'Linux' in platform.platform():
        if 'Ubuntu' in platform.platform():
            services_list = get_services_with_status()
        raid_data = get_raid_data()
        active_fans_count = get_fans_count()
        fans_count_range = range(active_fans_count)
    return render(request, 'status.html', locals())


def get_fans_count():
    active_fans_count = 0
    for fans_list in psutil.sensors_fans().values():
        for fan in fans_list:
            if fan.current > 0:
                active_fans_count += 1
    return active_fans_count


def get_ram_usage():
    memory = psutil.virtual_memory()
    data = {}
    data['units'] = 'GB'
    data['total'] = round(memory.total / 1073741824, 2)
    data['available'] = round(memory.available / 1073741824, 2)
    data['percent'] = memory.percent
    data['used'] = round(memory.used / 1073741824, 2)
    data['free'] = round(memory.free / 1073741824, 2)
    return data


def get_raid_data():
    try:
        raid_data = check_output(["cat", "/proc/mdstat"]) \
            .decode("utf-8").split("\n")
    except CalledProcessError:
        raid_data = ['RAID data not found']
    return raid_data


def get_disk_usage():
    disk_partitions = psutil.disk_partitions()
    data = {}
    for partition in disk_partitions:
        try:
            total = psutil.disk_usage(partition.mountpoint).total
            used = psutil.disk_usage(partition.mountpoint).used
            free = psutil.disk_usage(partition.mountpoint).free
            percent = psutil.disk_usage(partition.mountpoint).percent
            data[partition.device] = {
                'units': 'GB',
                'total': round(total / 1073741824, 2),
                'used': round(used / 1073741824, 2),
                'free': round(free / 1073741824, 2),
                'percent': percent
            }
        except PermissionError:
            logger.error(
                'Permission denied while reading {}'.format(partition))
    return data


def get_uptime():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    minutes, seconds = divmod(int(uptime.total_seconds()), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    data = {}
    data['weeks'] = weeks
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
        service_data = check_output(["grep", "Active"],
                                    stdin=service_data.stdout).decode("utf-8")
        service_data = service_data.replace("\n", '')
    except CalledProcessError:
        service_data = 'Service not found'
    return service_data
