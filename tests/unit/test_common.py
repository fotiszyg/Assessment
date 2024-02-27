from datetime import datetime

import pytest

from backup_manager.common import convert_to_datetime, convert_difference, get_week_occurrences


def test_convert_to_datetime():
    timestamp = "2024-02-22 03:01:32.542"
    datetime_object = convert_to_datetime(timestamp)
    assert datetime_object.date() == datetime(2024, 2, 22).date()
    assert datetime_object.year == 2024
    assert datetime_object.month == 2
    assert datetime_object.day == 22


@pytest.mark.parametrize(
    'new_time_string, old_time_string, exp_difference',
    [
        ('2024-02-24 03:01:32.542', '2024-02-22 03:01:32.542', '48:0:0.0'),
        ('2024-02-24 03:01:32.542', '2024-02-22 07:06:32.310', '43:55:0.232000'),
        ('2024-02-24 03:01:32.542', '2024-02-24 02:06:22.110', '0:55:10.432000')
    ]
)
def test_convert_difference(new_time_string, old_time_string, exp_difference):
    new_timestamp = convert_to_datetime(new_time_string)
    old_timestamp = convert_to_datetime(old_time_string)
    difference = new_timestamp - old_timestamp
    dif_string = convert_difference(difference)
    assert dif_string == exp_difference


def test_get_week_occurrences():
    week_list = [8, 32, 23, 10, 1, 30, 30, 30]
    week_1 = 10
    week_2 = 30
    occur = get_week_occurrences(week_1, week_list)
    assert len(occur) == 1
    assert occur[0] == 3
    occur = get_week_occurrences(week_2, week_list)
    assert len(occur) == 3
    assert occur[0] == 5
    assert occur[1] == 6
    assert occur[2] == 7
