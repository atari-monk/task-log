from datetime import datetime
from task_log.cli_controller.project_cli_controller import ProjectCliController
from task_log.cli_controller.task_cli_controller import TaskCliController
from task_log.crud.record_crud import RecordCrud
from task_log.json_db.db_info import DbInfo
from task_log.models.project import Project
from task_log.models.record import Record
from task_log.models.task import Task


class RecordCliController:
    def __init__(
        self,
        db_info: DbInfo,
        record_crud: RecordCrud,
        proj_cli_controller: ProjectCliController,
        task_cli_controller: TaskCliController,
    ):
        self._db_info = db_info
        self._proj_table = db_info.proj_table
        self._record_crud = record_crud
        self._proj_cli_controller = proj_cli_controller
        self._task_cli_controller = task_cli_controller

    def from_cli_input(self) -> None:
        project = self._proj_cli_controller.select_project()
        task = self._task_cli_controller.select_task(project)
        record_table = self._db_info.get_record_table(project.name)

        def get_id():
            return {"id": Record._get_next_id(record_table.path)}

        def get_date():
            value = datetime.now().strftime("%Y-%m-%d")
            return {
                "date": Record._get_string_input(
                    f"Date (YYYY-MM-DD) [default: {value}]: ", "date", allow_empty=True, default_value=value
                )
            }

        def get_task_id():
            return {"task_id": task.id}

        def get_description():
            return {
                "description": Record._get_string_input(
                    "Description: ", "description", max_length=300, allow_empty=True
                )
            }

        def get_estimate_minutes():
            return {
                "estimate_minutes": self._get_positive_integer_input(
                    "Estimated minutes: ", "estimate_minutes"
                )
            }

        def get_start_time():
            value = datetime.now().strftime("%H:%M")
            return {
                "start_time": Record._get_string_input(
                    f"Start time (HH:MM) [default: {value}]: ", "start_time", allow_empty=True, default_value=value
                )
            }

        new_record = Record.from_cli_input(
            record_table.path,
            [
                get_id,
                get_task_id,
                get_date,
                get_description,
                get_estimate_minutes,
                get_start_time,
            ],
        )
        print(f"Adding new Record")
        print("-" * 20)
        self._record_crud.create(project, new_record)

    def _update_from_cli(self, record: Record) -> None:
        def get_end_time():
            value = datetime.now().strftime("%H:%M")
            return {
                "end_time": record._get_string_input(
                    f"End time (HH:MM) [default: {value}]: ",
                    "end_time",
                    default_value=value,
                )
            }

        def get_note():
            return {
                "note": record._get_string_input(
                    f"Note [current: {record.note}]: ",
                    "note",
                    max_length=300,
                    allow_empty=True,
                    default_value=record.note,
                )
            }

        inputs = {}
        for method in [get_end_time, get_note]:
            inputs.update(method())

        record.end_time = inputs["end_time"]
        record.note = inputs["note"]
        if record.start_time and record.end_time:
            record._calculate_actual_minutes()

    def _get_positive_integer_input(self, prompt: str, field_name: str) -> int:
        while True:
            try:
                value = input(prompt).strip()
                if not value:
                    raise ValueError(f"{field_name} cannot be empty")
                value = int(value)
                Record._validate_positive_integer(value, field_name)
                return value
            except ValueError as e:
                print(f"Invalid input: {e}")
                print("Please try again.\n")

    def update_record(self):
        project = self._proj_cli_controller.select_project()
        task = self._task_cli_controller.select_task(project)
        records = self._record_crud.get_by_project(project)

        open_records = [r for r in records if r.task_id == task.id and not r.end_time]
        if not open_records:
            print(f"No open records found for task: {task.name}")
            return
        if len(open_records) > 1:
            print(
                f"Warning: Found {len(open_records)} open records for task {task.name}. Expected only one."
            )
            return

        record_to_update = open_records[0]
        print(f"Update Record")
        print("-" * 20)
        self._update_from_cli(record_to_update)
        self._record_crud.update(project, record_to_update)

    def print_records_of_project(
        self, project: Project = None, task: Task = None, records: Record = None
    ):
        if project is None:
            project = self._proj_cli_controller.select_project()
        if task is None:
            task = self._task_cli_controller.select_task(project)
        if records is None:
            records = self._record_crud.get_by_project(project)
        print(f"\nRecords of {project.name}")
        print("-" * 20)
        records = [record for record in records if record.task_id == task.id]
        print(Record.get_table_string(records) + "\n")

    def print_all(self, items: list[Record] = None):
        if items is None:
            items = self._record_crud.get_all()
        print(f"\nRecords")
        print("-" * 20)
        print(Record.get_table_string(items) + "\n")