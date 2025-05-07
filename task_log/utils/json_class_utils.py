import json
from pathlib import Path
from typing import List, Type
from task_log.utils.types import T


def load_from_json(cls: Type[T], file_path: Path) -> List[T]:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON data should be a list of items")

    if hasattr(cls, 'from_dict'):
        return [cls.from_dict(item) for item in data]
    
    return [cls(**item) for item in data]


def save_to_json(
    cls: Type[T], items: List[T], file_path: Path, indent: int = 2
) -> None:
    if not isinstance(items, list):
        raise ValueError("Items to save must be a list")

    new_data = [item.__dict__ for item in items if isinstance(item, cls)]
    if len(new_data) != len(items):
        raise ValueError(f"All items must be instances of {cls.__name__}")

    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=indent, ensure_ascii=False)
    except (IOError, TypeError) as e:
        raise IOError(f"Failed to save JSON to {file_path}: {str(e)}")


def append_to_json(
    cls: Type[T], new_items: List[T], file_path: Path, indent: int = 2
) -> None:
    if not isinstance(new_items, list):
        raise ValueError("Items to append must be a list")

    existing_items = []
    if file_path.exists():
        try:
            existing_items = load_from_json(cls, file_path)
        except (json.JSONDecodeError, IOError) as e:
            raise IOError(f"Failed to load existing JSON from {file_path}: {str(e)}")

    combined_items = existing_items + new_items
    save_to_json(cls, combined_items, file_path, indent)


@staticmethod
def update_in_json(
    cls: Type[T], item: T, file_path: Path, id_field: str = "id"
) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    items = load_from_json(cls, file_path)
    updated = False

    for i, existing_item in enumerate(items):
        if hasattr(existing_item, id_field) and hasattr(item, id_field):
            if getattr(existing_item, id_field) == getattr(item, id_field):
                items[i] = item
                updated = True
                break

    if not updated:
        raise ValueError("Item not found in JSON file")

    save_to_json(cls, items, file_path)

def delete_from_json(
    cls: Type[T], 
    item_id: int, 
    file_path: Path, 
    id_field: str = "id"
) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        items = load_from_json(cls, file_path)
    except (json.JSONDecodeError, IOError) as e:
        raise IOError(f"Failed to load JSON from {file_path}: {str(e)}")

    original_length = len(items)
    items = [item for item in items if getattr(item, id_field) != item_id]

    if len(items) == original_length:
        raise ValueError(f"Item with {id_field}={item_id} not found in JSON file")

    save_to_json(cls, items, file_path)