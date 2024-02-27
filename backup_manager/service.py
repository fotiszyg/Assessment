import logging
from datetime import datetime
from typing import Tuple, Any, Union

from classes import InstanceCustom, SnapshotCustom
from common import fetch_snapshots, get_week_occurrences
from delete import delete_snapshot

now = datetime.now()


def apply_daily_weekly_policy(
        project: str,
        inst: InstanceCustom,
        flag: bool
):
    snapshots = fetch_snapshots(project)
    # Lists with details of snapshot
    sn_names = []
    sn_dates = []
    sn_week = []
    sn_timestamp = []
    for shot in snapshots:
        if shot.source_disk != inst.disk:
            continue
        elif shot.source_disk == inst.disk and flag:
            flag = False
            logging.info('Checking backups for disk %s', shot.source_disk_id)
        custom_snap = SnapshotCustom(shot)
        difference = now - custom_snap.timestamp
        if difference.days < 7 and custom_snap.date in sn_dates:
            logging.info('Found 2 snapshots made between %s and %s days ago',
                         difference.days, difference.days + 1)
            # If there is another snapshot for one specific day in the last 7 days, check what is the most recent.
            # If details of this exist in the lists, delete the snapshot from the sn_names list and clear the lists,
            # otherwise delete the last checked snapshot.
            sn_names, sn_dates, sn_week, sn_timestamp = delete_snapshot_from_policy(
                sn_names, sn_dates, sn_week, sn_timestamp, custom_snap, project)
        elif difference.days > 7 and custom_snap.week in sn_week:
            sn_names, sn_dates, sn_week, sn_timestamp = apply_week_policy(
                sn_names, sn_dates, sn_week, sn_timestamp, custom_snap, project)
        else:
            # If snapshot is the only snapshot for one specific day or a week
            # (for snapshots older than 7 days), append the details in the lists
            sn_names.append(custom_snap.name)
            sn_dates.append(custom_snap.date)
            sn_week.append(custom_snap.week)
            sn_timestamp.append(custom_snap.timestamp)


def delete_snapshot_from_policy(sn_names: list, sn_dates: list, sn_week: list, sn_timestamp: list,
                                custom_snapshot: SnapshotCustom, project: str, ind: int = None) -> \
        Tuple[Union[list, Any], Union[list, Any], Union[list, Any], Union[list, Any]]:
    if not ind:
        ind = sn_dates.index(custom_snapshot.date)
    if sn_timestamp[ind] < custom_snapshot.timestamp:
        name = sn_names[ind]
        logging.info('Deleting snapshot %s', name)
        sn_names.pop(ind)
        sn_dates.pop(ind)
        sn_week.pop(ind)
        sn_timestamp.pop(ind)
        delete_snapshot(project, name)
    else:
        name = custom_snapshot.name
        logging.info('Deleting snapshot %s', name)
        delete_snapshot(project, name)
    return sn_names, sn_dates, sn_week, sn_timestamp


def apply_policy(sn_names: list, sn_dates: list, sn_week: list, sn_timestamp: list, index: int,
                 custom_snapshot: SnapshotCustom, project: str) -> \
        Tuple[Union[list, Any], Union[list, Any], Union[list, Any], Union[list, Any]]:
    if custom_snapshot.date.year == sn_dates[index].year:
        logging.info('Found 2 snapshots made in week %s of year %s',
                     custom_snapshot.week, custom_snapshot.date.year)
        sn_names, sn_dates, sn_week, sn_timestamp = (
            delete_snapshot_from_policy(
                sn_names, sn_dates, sn_week, sn_timestamp, custom_snapshot, project, index))
    else:
        # If week of the last checked snapshot is in a different year, update lists
        sn_names.append(custom_snapshot.name)
        sn_dates.append(custom_snapshot.date)
        sn_week.append(custom_snapshot.week)
        sn_timestamp.append(custom_snapshot.timestamp)
    return sn_names, sn_dates, sn_week, sn_timestamp


def apply_week_policy(sn_names: list, sn_dates: list, sn_week: list, sn_timestamp: list,
                      custom_snapshot: SnapshotCustom, project: str) -> \
        Tuple[Union[list, Any], Union[list, Any], Union[list, Any], Union[list, Any]]:
    # If there are multiple entries for a specific week, get all indexes from sn_week
    occur = get_week_occurrences(custom_snapshot.week, sn_week)
    if len(occur) == 1:
        sn_names, sn_dates, sn_week, sn_timestamp = (
            apply_policy(
                sn_names, sn_dates, sn_week, sn_timestamp, occur[0], custom_snapshot, project))
    else:
        for i in occur:
            sn_names, sn_dates, sn_week, sn_timestamp = (
                apply_policy(
                    sn_names, sn_dates, sn_week, sn_timestamp, i, custom_snapshot, project))
    return sn_names, sn_dates, sn_week, sn_timestamp
