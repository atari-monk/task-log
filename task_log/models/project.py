from typing import List
from dataclasses import dataclass, field
from task_log.models.base_model import BaseModel


@dataclass
class Project(BaseModel):
    id: int
    name: str
    description: str
    repository_name: str = field(default="")

    def __post_init__(self):
        self._validate_string(
            self.name, "name", max_length=50
        )
        self._validate_string(
            self.repository_name, "repository_name", max_length=50, 
            must_be_lowercase=True, no_spaces=True
        )
        self._validate_string(self.description, "description", max_length=300)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            repository_name=data.get('repository_name', '')
        )

    @staticmethod
    def get_table_string(items: List["Project"]) -> str:
        columns = [
            ("Id", "id", int), 
            ("Name", "name"), 
            ("Description", "description"), 
            ("Repository", "repository_name")
        ]
        return Project.generate_table_string(items, columns)