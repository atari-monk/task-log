from pathlib import Path
from typing import Callable
from task_log.json_db.db_path import DbPath


class DbTablePath:
    def __init__(
        self, db_path: DbPath, name_func: Callable[[], str], ext: str = "json"
    ):
        self.db_path = db_path
        self.name_func = name_func
        self.ext = ext
        self._initialize_file()

    @property
    def path(self) -> Path:
        return self.db_path.path / f"{self.name_func()}.{self.ext}"

    def _initialize_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]")

    def get_path(self) -> Path:
        return self.path
