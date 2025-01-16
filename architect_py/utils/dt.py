from datetime import date, datetime, timezone


def get_expiration_from_CME_name(name: str) -> date:
    _, d, *_ = name.split(" ")

    return datetime.strptime(d, "%Y%m%d").date()


def convert_datetime_to_utc_str(dt: datetime):
    if dt.tzinfo is None:
        raise ValueError(
            "in client requests, the datetime objects must be timezone-aware. Try \n"
            "import pytz\n"
            "datetime(..., tzinfo=your_local_timezone)\n"
            "# datetime.now(your_local_timezone)"
            "# examples of local timezones: pytz.timezone('US/Eastern'), "
            "pytz.timezone('US/Pacific'), pytz.timezone('US/Central')\n"
            "# with python3.9+, you can use the zoneinfo module, which is part of the standard library\n"
            "# and thus does not require installing pytz\n"
        )
    utc_str = dt.astimezone(timezone.utc).isoformat()[:-6]
    # [:-6] removes the utc offset

    return f"{utc_str}Z"
