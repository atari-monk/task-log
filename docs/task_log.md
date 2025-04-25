# Task Log Script.

Cli to track task time.

## Assumptions:

- Development Process:
  1. Write unit tests first.
  2. Write feature code to pass tests.
- Code Style:
  - python.
  - No comments, self-documenting code only.

## Paths:

- class DbPath.

  - constructing db path.
  - repoPath.
  - dbFolder.
  - properties:
  - path = RepoPath + DbFolder.
  - methods:
    - check/generate folders in ctor.

- class DbTablePath.
  - constructing db table path.
  - parameters:
  - dbPath of type DbPath.
  - namingLogic - lambda to generate name.
  - methods:
  - getPath.
    - ext - file extension param, defaults to 'json'.
    - uses parameters to return table path.

## Models:

- dataclass Project, Task, Record.

  ```json
  [
    {
      "Id": "Some Standard Format for id",
      "Name": "Project Name",
      "Description": "Max 300 characters"
    }
  ]
  ```

  ```json
  [
    {
      "Id": "Some Standard Format for id",
      "ProjectId": "Some Standard Format for id",
      "Name": "Task Name",
      "Description": "Max 300 characters"
    }
  ]
  ```

  ```json
  [
    {
      "Date": "2025-04-17",
      "TaskId": "1",
      "Description": "Max 300 characters",
      "Estimate Minutes": 0,
      "Start Time": "19:03",
      "End Time": "20:55",
      "Actual Minutes": 0,
      "Note": "Max 300 characters"
    }
  ]
  ```

- shared methods:

  - validation methods.
  - loading List[ModelType] from json file.
  - get string with objects list.

- Record methods:
  - method loading last record from json file.
