import logging
from datetime import datetime

from google.cloud.compute_v1 import SnapshotsClient, Snapshot

from assignment_1 import list_instances
from classes import InstanceCustom
from common import convert_to_datetime, convert_difference

now = datetime.now()

logging.basicConfig(format='%(asctime)s %(levelname)s  %(message)s', level=logging.INFO)


def create_snapshot(
        inst: InstanceCustom,
        snapshot_client,
        name: str,
        count: int,
        project: str,
) -> int:
    if inst.backup_enabled and inst.last_backup != 'Never':
        # Find difference between today and most recent backup.
        # Creation timestamp needs to be converted to datetime object.
        # For this T is removed and also the last 6 characters are ignored.
        created_at = convert_to_datetime(inst.last_backup.replace('T', ' ')[:-6])
        difference = now - created_at
        logging.info('Last backup was %s ago', convert_difference(difference))
        if not difference.days:
            # If last snapshot was created earlier than one day, create a new one
            count += 1
            logging.info('Starting asynchronous backup creation')
            snap = Snapshot()
            snap.source_disk = inst.disk
            snap.name = name
            operation = snapshot_client.insert(project=project, snapshot_resource=snap)
            # Currently asynchronous operation not working because of authentication issues
            # sample_wait(operation, project, zone, inst.disk.split('/')[-1])
        elif not difference.days:
            logging.info('Skipping backup creation since the last backup is too recent')
    return count


def snapshot(project: str, zone: str, name: str):
    """
    This method creates a snapshot for an instance if backup is enabled and
    last snapshot was created for more than one day before current time.
    :param name: Name of snapshot to be created
    :param project: Name of project
    :param zone: Name of zone

    """
    logging.info('Starting backup process')
    instances = list_instances(project, zone)
    logging.info('Found %s instances', len(instances))
    snapshot_client = SnapshotsClient.from_service_account_json('xcc-fotis.json')
    count = 0
    for inst in instances:
        # Iterate over list of instances to find whether they have at least one snapshot during last day
        logging.info('Instance: %s', inst.name)
        logging.info('Backup Enabled: %s', inst.backup_enabled)
        count = create_snapshot(inst, snapshot_client, name, count, project)
    if count:
        # If there is at least one snapshot created, log following message
        logging.info('All snapshots done')
    # return snapshot_client.get(project='xcc-fotis', snapshot="second-snapshot")


if __name__ == '__main__':
    snapshot('xcc-fotis', 'europe-west4-a', 'second-snapshot')
