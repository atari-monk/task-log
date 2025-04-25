from pathlib import Path


class DbPath:
    def __init__(self, repo_path: Path, db_folder: str):
        if isinstance(repo_path, str):
            repo_path = Path(repo_path)
        self.repo_path = repo_path
        self.db_folder = db_folder
        self.path.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self.repo_path / self.db_folder
