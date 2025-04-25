from task_log.json_db.db_info import DbInfo
from task_log.models.project import Project
from task_log.models.record import Record


class RecordCrud:
    def __init__(self, db_info: DbInfo):
        self._db_info = db_info

    def create(self, project: Project, record: Record):
        record_table = self._db_info.get_record_table(project.name)
        Record.append_to_json([record], record_table.path)

    def update(self, project: Project, record: Record):
        record_table = self._db_info.get_record_table(project.name)
        Record.update_in_json(record, record_table.path)

    def get_all(self, project: Project):
        record_table = self._db_info.get_record_table(project.name)
        return Record.load_from_json(record_table.path)
