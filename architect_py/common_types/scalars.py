from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from architect_py.graphql_client.base_model import UnsetType


def convert_datetime_to_utc_str(dt: "Optional[datetime] | UnsetType") -> Optional[str]:
    if not isinstance(dt, datetime):
        return None

    if dt.tzinfo is None:
        raise ValueError(
            "in a datetime sent to the backend, the good_til_date must be timezone-aware. Try \n"
            "from zoneinfo import ZoneInfo\n"
            "datetime(..., tzinfo={your_local_timezone}) or "
            "datetime.now(tz=ZoneInfo('UTC'))\n"
            "# examples of local timezones:\n"
            "ZoneInfo('America/New_York'), "
            "ZoneInfo('America/Los_Angeles'), ZoneInfo('America/Chicago')"
        )
    utc_str = dt.astimezone(timezone.utc).isoformat()[:-6]
    # [:-6] removes the utc offset

    return f"{utc_str}Z"
