from task_log.json_db.db_info import DbInfo
from task_log.models.project import Project


class ProjectCrud:
    def __init__(self, db_tables: DbInfo):
        self._proj_table = db_tables.proj_table

    def create(self, project: Project):
        Project.append_to_json([project], self._proj_table.path)

    def get_all(self):
        return Project.load_from_json(self._proj_table.path)
