import logging
from datetime import datetime

import click

from assignment_1 import list_instances_no_backup
from service import apply_daily_weekly_policy


logging.basicConfig(format='%(asctime)s %(levelname)s  %(message)s', level=logging.INFO)

now = datetime.now()


@click.group()
def cli():
    pass


@cli.command('apply-retention-policy')
def apply_retention_policy():
    """
    Command that applies the retention policy for all snapshots in a project:
    1. No more than one backup per day should be kept for backups made in the last 7 days.
    2. No more than one backup per week should be kept for backups made prior to the last 7 days.
    """
    logging.info('Checking backups against retention policy')
    instances = list_instances_no_backup('xcc-fotis')
    for inst in instances:
        flag = True
        # flag is used to print a log message for a certain instance only once
        if not inst.backup_enabled:
            # Ignore instances when backup is not enabled
            continue
        apply_daily_weekly_policy('xcc-fotis', inst, flag)


if __name__ == '__main__':
    cli()
