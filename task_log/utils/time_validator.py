from datetime import datetime


def validate_date_string(
    value: str, field_name: str, date_format: str = "%Y-%m-%d"
) -> None:
    try:
        datetime.strptime(value, date_format)
    except ValueError:
        raise ValueError(f"Invalid {field_name} format, expected {date_format}")


def validate_time_string(
    value: str, field_name: str, time_format: str = "%H:%M"
) -> None:
    try:
        datetime.strptime(value, time_format)
    except ValueError:
        raise ValueError(f"Invalid {field_name} format, expected {time_format}")


def validate_time_range(
    start_time: str,
    end_time: str,
    start_field_name: str = "StartTime",
    end_field_name: str = "EndTime",
    time_format: str = "%H:%M",
) -> None:
    start = datetime.strptime(start_time, time_format)
    end = datetime.strptime(end_time, time_format)
    if end == start:
        raise ValueError(f"{end_field_name} cannot be equal to {start_field_name}")
