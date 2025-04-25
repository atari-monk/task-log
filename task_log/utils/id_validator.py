from pathlib import Path
from typing import Type
from task_log.utils.json_class_utils import load_from_json
from task_log.utils.types import T


def validate_ids(cls: Type[T], file_path: Path, id_field: str = "id") -> bool:
    items = load_from_json(cls, file_path)
    ids = [getattr(item, id_field) for item in items if hasattr(item, id_field)]
    return len(ids) == len(set(ids)) and all(isinstance(id, int) for id in ids)


def get_next_id(cls: Type[T], file_path: Path, id_field: str = "id") -> int:
    if not file_path.exists():
        return 1
    items = load_from_json(cls, file_path)
    if not items:
        return 1
    if not hasattr(items[0], id_field):
        raise AttributeError(f"Items must have an '{id_field}' attribute")
    return max(getattr(item, id_field) for item in items) + 1
