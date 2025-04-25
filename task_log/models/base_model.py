from typing import TypeVar, Type, List, Any, Callable
from pathlib import Path
from dataclasses import dataclass
from task_log.utils.class_to_table import generate_table_string
from task_log.utils.cli_input import from_cli_input, get_string_input
from task_log.utils.id_validator import get_next_id, validate_ids
from task_log.utils.int_validator import validate_positive_integer
from task_log.utils.json_class_utils import (
    append_to_json,
    load_from_json,
    save_to_json,
    update_in_json,
)
from task_log.utils.string_validator import validate_string
from task_log.utils.unique_field_validator import validate_unique_field

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    @staticmethod
    def _validate_positive_integer(value: Any, field_name: str) -> None:
        validate_positive_integer(value, field_name)

    @staticmethod
    def _validate_string(
        value: Any,
        field_name: str,
        max_length: int = None,
        must_be_lowercase: bool = False,
        no_spaces: bool = False,
    ) -> None:
        validate_string(
            value,
            field_name,
            max_length=max_length,
            must_be_lowercase=must_be_lowercase,
            no_spaces=no_spaces,
        )

    @classmethod
    def _validate_unique_field(
        cls: Type[T],
        file_path: Path,
        field_name: str,
        value: Any,
        case_sensitive: bool = True,
        error_message: str = None,
    ) -> None:
        validate_unique_field(
            cls,
            file_path,
            field_name,
            value,
            case_sensitive=case_sensitive,
            error_message=error_message,
        )

    @classmethod
    def _get_next_id(cls, file_path: Path) -> int:
        if not validate_ids(cls, file_path=file_path):
            raise ValueError(f"{file_path} has errors in Ids")
        return get_next_id(cls, file_path=file_path)

    @classmethod
    def from_dict(cls, data: dict) -> Any:
        return cls(**data)
    
    @classmethod
    def load_from_json(cls: Type[T], file_path: Path) -> List[T]:
        return load_from_json(cls, file_path)

    @classmethod
    def save_to_json(
        cls: Type[T], items: List[T], file_path: Path, indent: int = 2
    ) -> None:
        save_to_json(cls, items, file_path, indent)

    @classmethod
    def append_to_json(
        cls: Type[T], new_items: List[T], file_path: Path, indent: int = 2
    ) -> None:
        append_to_json(cls, new_items, file_path, indent)

    @classmethod
    def update_in_json(cls: Type[T], item: T, file_path: Path) -> None:
        update_in_json(cls, item, file_path)

    @classmethod
    def generate_table_string(cls, items: List[T], columns: list) -> str:
        return generate_table_string(cls, items, columns)

    @classmethod
    def _get_string_input(
        cls,
        prompt: str,
        field_name: str,
        max_length: int = None,
        must_be_lowercase: bool = False,
        no_spaces: bool = False,
        allow_empty: bool = False,
        default_value: str = None,
    ) -> str:
        return get_string_input(
            cls,
            prompt,
            field_name,
            max_length,
            must_be_lowercase,
            no_spaces,
            allow_empty,
            default_value,
        )

    @classmethod
    def from_cli_input(
        cls: Type[T], file_path: Path, input_methods: List[Callable]
    ) -> T:
        return from_cli_input(cls, file_path, input_methods)
