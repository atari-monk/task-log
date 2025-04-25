from task_log.crud.project_crud import ProjectCrud
from task_log.json_db.db_info import DbInfo
from task_log.models.project import Project


class ProjectCliController:
    def __init__(self, db_tables: DbInfo, proj_crud: ProjectCrud):
        self._proj_table = db_tables.proj_table
        self._proj_crud = proj_crud

    def from_cli_input(self) -> None:
        def get_id():
            return {"id": Project._get_next_id(self._proj_table.path)}

        def get_name():
            name = Project._get_string_input(
                "Name (max 50 chars): ",
                "name",
                max_length=50,
                allow_empty=False,
            )
            Project._validate_unique_field(self._proj_table.path, "name", name)
            return {"name": name}

        def get_description():
            return {
                "description": Project._get_string_input(
                    "Description (max 300 chars): ",
                    "description",
                    max_length=300,
                    allow_empty=False,
                )
            }

        def get_repository_name():
            return {
                "repository_name": Project._get_string_input(
                    "Repository name (max 50 chars, lowercase, no spaces): ",
                    "repository_name",
                    max_length=50,
                    must_be_lowercase=True,
                    no_spaces=True,
                    allow_empty=True,
                )
            }

        new_project = Project.from_cli_input(
            self._proj_table.path,
            input_methods=[get_id, get_name, get_description, get_repository_name]
        )
        print(f"Adding new Project")
        print("-" * 20)
        self._proj_crud.create(new_project)

    def select_project(self) -> "Project":
        projects = self._proj_crud.get_all()
        if not projects:
            raise ValueError("No projects available to select")

        self.print_all(projects)

        while True:
            try:
                selected_id = int(input("\nEnter project ID to select: "))
                for project in projects:
                    if project.id == selected_id:
                        return project
                raise ValueError("Invalid project ID")
            except ValueError as e:
                print(f"Invalid input: {e}")
                print("Please try again.")

    def print_all(self, projects: list[Project] = None):
        if projects is None:
            projects = self._proj_crud.get_all()
        print(f"\nProjects")
        print("-" * 20)
        print(Project.get_table_string(projects) + "\n")

    def print(self, project: Project):
        print(f"\nProject")
        print("-" * 20)
        print(Project.get_table_string([project]) + "\n")