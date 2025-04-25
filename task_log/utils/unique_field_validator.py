from pathlib import Path
from typing import Any, Type
from task_log.utils.json_class_utils import load_from_json
from task_log.utils.types import T


def validate_unique_field(
    cls: Type[T],
    file_path: Path,
    field_name: str,
    value: Any,
    case_sensitive: bool = True,
    error_message: str = None,
) -> None:
    if not file_path.exists():
        return

    items = load_from_json(cls, file_path)
    for item in items:
        existing_value = getattr(item, field_name)
        if (
            not case_sensitive
            and isinstance(value, str)
            and isinstance(existing_value, str)
        ):
            if value.lower() == existing_value.lower():
                raise ValueError(
                    error_message or f"{field_name} must be unique (case insensitive)"
                )
        elif value == existing_value:
            raise ValueError(error_message or f"{field_name} must be unique")
