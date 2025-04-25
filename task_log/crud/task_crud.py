from task_log.json_db.db_info import DbInfo
from task_log.models.project import Project
from task_log.models.task import Task


class TaskCrud:
    def __init__(self, db_tables: DbInfo):
        self._db_tables = db_tables
        self._proj_table = db_tables.proj_table

    def create(self, project: Project, task: Task):
        Task.append_to_json([task], self._db_tables.get_task_table(project.name).path)

    def get_all(self, project: Project):
        return Task.load_from_json(self._db_tables.get_task_table(project.name).path)

    def get_by_project(self, project: Project):
        return [task for task in self.get_all(project) if task.project_id == project.id]
