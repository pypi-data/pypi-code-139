""" __init__.py for the temporal package. """

# Standard Library
import datetime
from datetime import datetime as datetime_class
import sys
if sys.version_info.major != 3:
    raise Exception("Temporal is only available for Python 3.")

# Third Party
if sys.version_info.minor < 9:
    # https://pypi.org/project/pytz/
    import pytz  # pylint: disable=import-error
    from dateutil.tz import tzutc
else:
    from zoneinfo import ZoneInfo

from temporal import weeks  # pylint: disable=wrong-import-position

# Functions are defined in alphabetical order:


def date_to_iso_string(any_date):
    """
    Given a date, create an ISO String.  For example, 2021-12-26.
    """

    if not isinstance(any_date, datetime.date):
        raise Exception(f"Argument should be of type 'datetime.date', not '{type(any_date)}'")
    return any_date.strftime("%Y-%m-%d")


def datetime_to_sql_datetime(any_datetime: datetime):
    """
    Convert a Python DateTime into a DateTime that can be written to MariaDB/MySQL.
    """
    return any_datetime.strftime('%Y-%m-%d %H:%M:%S')


def get_system_date(time_zone):
    return get_system_datetime_now(time_zone).date()


def get_system_datetime_now(time_zone):
    """
    Given a dateutil.tz Time Zone, return the current DateTime.
    """
    # Get the current UTC datetime
    if sys.version_info.minor < 9:
		# Python 3.8 or less:
        utc_datetime = datetime_class.now(tzutc())
    else:
        # Python 3.9 or greater
        utc_datetime = datetime.now(ZoneInfo("UTC"))  # Get the current UTC datetime.

    return utc_datetime.astimezone(time_zone)  # Next, convert to the time_zone argument.


def is_datetime_naive(any_datetime):
    """
    Returns True if the datetime is missing a Time Zone component.
    """
    if not isinstance(any_datetime, datetime_class):
        raise TypeError("Argument 'any_datetime' must be a Python datetime object.")

    if any_datetime.tzinfo is None:
        return True
    return False


def make_datetime_naive(any_datetime):
    """
    Takes a timezone-aware datetime, and makes it naive.
    """
    return any_datetime.replace(tzinfo=None)


def make_datetime_tz_aware(naive_datetime):
    """
    Add the ERP system time zone to any naive datetime.
    """
    if naive_datetime.tz_info:
        raise Exception("Datetime is already localized and time zone aware.")


def safeset(any_dict, key, value, as_value=False):
    """
    This function is used for setting values on an existing Object, while respecting current keys.
    """

    if not hasattr(any_dict, key):
        raise AttributeError(f"Cannot assign value to unknown attribute '{key}' in dictionary {any_dict}.")
    if isinstance(value, list) and not as_value:
        any_dict.__dict__[key] = []
        any_dict.extend(key, value)
    else:
        any_dict.__dict__[key] = value
