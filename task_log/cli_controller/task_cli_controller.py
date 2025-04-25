from task_log.cli_controller.project_cli_controller import ProjectCliController
from task_log.crud.task_crud import TaskCrud
from task_log.json_db.db_info import DbInfo
from task_log.models.task import Task


class TaskCliController:
    def __init__(
        self,
        db_info: DbInfo,
        task_crud: TaskCrud,
        proj_cli_controller: ProjectCliController,
    ):
        self._db_info = db_info
        self._proj_table = db_info.proj_table
        self._task_crud = task_crud
        self._proj_cli_controller = proj_cli_controller

    def from_cli_input(self) -> None:
        project = self._proj_cli_controller.select_project()
        task_table = self._db_info.get_task_table(project.name)

        def get_id():
            return {"id": Task._get_next_id(task_table.path)}

        def get_project_id():
            return {"project_id": project.id}

        def get_name():
            return {
                "name": Task._get_string_input(
                    "Name (max 100 chars): ", "name", max_length=100
                )
            }

        def get_description():
            return {
                "description": Task._get_string_input(
                    "Description (max 300 chars): ", "description", max_length=300
                )
            }

        new_task = Task.from_cli_input(
            task_table.path,
            [get_id, get_project_id, get_name, get_description],
        )
        print(f"Adding new Task")
        print("-" * 20)
        self._task_crud.create(project, new_task)

    def select_task(self, project=None) -> "Task":
        if project is None:
            project = self._proj_cli_controller.select_project()

        tasks = self._task_crud.get_all(project)
        if not tasks:
            raise ValueError("No tasks available to select")

        self.print_tasks_of_project(project, tasks)

        while True:
            try:
                selected_id = int(input("\nEnter task ID to select: "))
                for task in tasks:
                    if task.id == selected_id:
                        return task
                raise ValueError("Invalid task ID")
            except ValueError as e:
                print(f"Invalid input: {e}")
                print("Please try again.")

    def print_tasks_of_project(self, project=None, tasks=None):
        if project is None:
            project = self._proj_cli_controller.select_project()
        if tasks is None:
            tasks = self._task_crud.get_all(project)
        print(f"\nTasks of {project.name}")
        print("-" * 20)
        print(Task.get_table_string(tasks) + "\n")

    def print(self, task: Task):
        print(f"\nTask")
        print("-" * 20)
        print(Task.get_table_string([task]) + "\n")
