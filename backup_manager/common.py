import logging
from datetime import datetime, timedelta
from typing import Tuple, Union, Any

from google.cloud.compute_v1 import InstancesClient, SnapshotsClient, WaitZoneOperationRequest, ZoneOperationsClient
from google.cloud.compute_v1.services.instances.pagers import ListPager as ListOfInstances
from google.cloud.compute_v1.services.snapshots.pagers import ListPager as ListOfSnapshots


now = datetime.now()


def fetch_vms(project: str, zone: str) -> ListOfInstances:
    c = InstancesClient.from_service_account_json('xcc-fotis.json')
    instances = c.list(project=project, zone=zone)
    return instances


def fetch_snapshots(project: str) -> ListOfSnapshots:
    c = SnapshotsClient.from_service_account_json('xcc-fotis.json')
    snapshots = c.list(project=project)
    return snapshots


def convert_to_datetime(timestamp: str) -> datetime:
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    return datetime.strptime(timestamp, datetime_format)


def convert_difference(diff: timedelta, h: int = 0) -> str:
    diff.total_seconds()
    if diff.days:
        h = 24 * int(diff.days)
    h = h + int(diff.seconds // 3600)
    m = int((diff.seconds % 3600) // 60)
    sec = int((diff.seconds % 3600) % 60)
    return f"{h}:{m}:{sec}.{diff.microseconds}"


def sample_wait(operation, project, zone, disk):
    # Create a client
    client = ZoneOperationsClient()

    # Initialize request argument(s)
    request = WaitZoneOperationRequest(
        operation=operation,
        project=project,
        zone=zone,
    )

    # Make the request
    logging.info("Snapshot for disk %s is Status.%s", disk)
    client.wait(request=request)
    logging.info("Snapshot for disk %s is Status1", disk)


def get_week_occurrences(week: int, sn_week: list) -> list:
    occurrences = [i for i, n in enumerate(sn_week) if n == week]
    return occurrences
