from typing import Any


def validate_string(
    value: Any,
    field_name: str,
    max_length: int = None,
    must_be_lowercase: bool = False,
    no_spaces: bool = False,
) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    if max_length is not None and len(value) > max_length:
        raise ValueError(f"{field_name} cannot exceed {max_length} characters")

    if must_be_lowercase and value != value.lower():
        raise ValueError(f"{field_name} must be lowercase")

    if no_spaces and " " in value:
        raise ValueError(f"{field_name} must not contain spaces")
