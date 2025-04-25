from typing import List
from task_log.utils.types import T


def generate_table_string(cls, items: List[T], columns: list) -> str:
    if not items:
        return f"No {cls.__name__.lower()}s to list"

    max_lengths = []
    for col in columns:
        header, field_name, *rest = col
        max_len = len(header)
        format_func = rest[0] if rest else None
        for item in items:
            value = getattr(item, field_name)
            if format_func:
                value = format_func(value)
            value_len = len(str(value))
            if value_len > max_len:
                max_len = value_len
        max_lengths.append(max_len)

    header_parts = []
    for i, (header, _, *_) in enumerate(columns):
        header_parts.append(f"{header:<{max_lengths[i]}}")
    header = "  ".join(header_parts)

    separator = "-" * len(header)
    lines = [header, separator]

    for item in items:
        line_parts = []
        for i, (_, field_name, *rest) in enumerate(columns):
            value = getattr(item, field_name)
            if rest:
                value = rest[0](value)
            line_parts.append(f"{str(value):<{max_lengths[i]}}")
        lines.append("  ".join(line_parts))

    return "\n".join(lines)
