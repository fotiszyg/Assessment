from datetime import datetime
from google.cloud.compute_v1.services.snapshots.pagers import ListPager
from prettytable import PrettyTable

from classes import InstanceCustom
from common import fetch_vms, fetch_snapshots, convert_to_datetime

now = datetime.now()


def list_instances_no_backup(project: str) -> list:
    """

    :param project: Name of project
    :return: List of custom instance objects without information about most recent backup
    """
    instances = fetch_vms(project, 'europe-west4-a')
    list_of_instances = []
    for inst in instances:
        instance = InstanceCustom(
            name=inst.name,
            disk=inst.disks[0].source
        )
        if inst.labels['backup'] == 'true':
            instance.backup_enabled = True
        list_of_instances.append(instance)
    return list_of_instances


def get_most_recent_backup(
        label: str,
        instance: InstanceCustom,
        snapshots: ListPager
) -> InstanceCustom:
    list_snapshots = []
    if label == 'true':
        instance.backup_enabled = True
        for sn in snapshots:
            if sn.source_disk == instance.disk:
                # Creation timestamp needs to be converted to datetime object.
                # For this T is removed and also the last 6 characters are ignored.
                created_at = convert_to_datetime(sn.creation_timestamp.replace('T', ' ')[:-6])
                list_snapshots.append(created_at)
            else:
                continue
    if list_snapshots:
        # Find most recent backup time and convert it back to a string similar to what was asked.
        last_backup = max(list_snapshots)
        instance.last_backup = last_backup.strftime("%Y-%m-%d %H:%M:%S.%f") + '-08:00'
    return instance


def list_instances(project: str, zone: str) -> list:
    """
    :param project:
    :param zone:
    :return: List of custom Instance objects
    """
    # Get list of instances and snapshots
    instances = fetch_vms(project, zone)
    snapshots = fetch_snapshots(project)
    list_of_instances = []
    for inst in instances:
        # Create a custom instance object
        instance = InstanceCustom(
            name=inst.name,
            disk=inst.disks[0].source
        )
        instance = get_most_recent_backup(inst.labels['backup'], instance, snapshots)
        list_of_instances.append(instance)
    return list_of_instances


def print_table_of_instances(project: str, zone: str):
    """
    This method prints a table with the attributes of each custom instance object inside a project
    """
    list_of_instances = list_instances(project, zone)
    t = PrettyTable(['Name', 'Backup Enabled', 'Disk', 'Last Backup'])
    for ins in list_of_instances:
        t.add_row([ins.name, ins.backup_enabled, ins.disk.split('/')[-1], ins.last_backup])
    print(t)


if __name__ == '__main__':
    print_table_of_instances('xcc-fotis', 'europe-west4-a')
