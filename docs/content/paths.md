# Paths

## class DbPath

- constructing db path
- repoPath
- dbFolder
- path = RepoPath + DbFolder
- check/generate folders in ctor

## class DbTablePath

- constructing db table path
- dbPath of type DbPath
- namingLogic - lambda to generate name
- getPath
    - ext - file extension param, defaults to 'json'
    - uses parameters to return table path
