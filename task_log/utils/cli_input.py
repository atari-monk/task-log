from pathlib import Path
from typing import Callable, List, Type
from task_log.utils.types import T


def get_string_input(
    cls,
    prompt: str,
    field_name: str,
    max_length: int = None,
    must_be_lowercase: bool = False,
    no_spaces: bool = False,
    allow_empty: bool = False,
    default_value: str = None,
) -> str:
    while True:
        try:
            value = input(prompt).strip()
            if not value and default_value is not None:
                cls._validate_string(
                    default_value,
                    field_name,
                    max_length=max_length,
                    must_be_lowercase=must_be_lowercase,
                    no_spaces=no_spaces,
                )
                return default_value
            if not value and not allow_empty:
                raise ValueError(f"{field_name} cannot be empty")
            cls._validate_string(
                value,
                field_name,
                max_length=max_length,
                must_be_lowercase=must_be_lowercase,
                no_spaces=no_spaces,
            )
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")
            print("Please try again.\n")


def from_cli_input(cls: Type[T], file_path: Path, input_methods: List[Callable]) -> T:
    inputs = {}
    for method in input_methods:
        result = method()
        inputs.update(result)
    return cls(**inputs)
