from common import (convert_to_datetime)


class InstanceCustom:
    """
    A custom Instance object for easier handling.

    Attributes:
        name: Name of the instance (string).
        disk: Name of the disk - retrieved from disks['source'] property (string).
        backup_enabled: Label that indicates whether it is possible for an instance to have a backup (boolean).
        last_backup: Date of most recent backup for an instance.
                     If there is no backup or backup is not enabled, value is Never (string).
    """

    def __init__(self, name, disk, backup_enabled=False, last_backup='Never'):
        self.name = name
        self.disk = disk
        self.backup_enabled = backup_enabled
        self.last_backup = last_backup


class SnapshotCustom:
    """
        A custom Snapshot object for easier handling.

        Attributes:
            name: Name of the snapshot (string).
            timestamp: Creation timestamp of the snapshot (datetime object).
            date: Date of snapshot's creation - timestamp without time, only date details (str).
            week: Week when snapshot was created (int).
        """
    def __init__(self, snapshot):
        self.name = snapshot.name
        self.timestamp = convert_to_datetime(snapshot.creation_timestamp.replace('T', ' ')[:-6])
        self.date = self.timestamp.date()
        self.week = self.date.isocalendar()[1]
