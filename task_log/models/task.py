from pathlib import Path
from typing import List
from dataclasses import dataclass
from task_log.models.base_model import BaseModel


@dataclass
class Task(BaseModel):
    id: int
    project_id: int
    name: str
    description: str

    def __post_init__(self):
        self._validate_string(self.name, "name", max_length=100)
        self._validate_string(self.description, "description", max_length=300)

    @staticmethod
    def get_table_string(items: List["Task"]) -> str:
        columns = [
            ("Id", "id", int),
            ("Project Id", "project_id", int),
            ("Name", "name"),
            ("Description", "description"),
        ]
        return Task.generate_table_string(items, columns)
