import pytest
import shutil
import tempfile
from pathlib import Path
from task_log.json_db.db_path import DbPath


@pytest.fixture
def temp_dir():
    test_dir = tempfile.mkdtemp()
    yield test_dir
    shutil.rmtree(test_dir)


def test_init_creates_directory(temp_dir):
    db_info = DbPath(Path(temp_dir), "")
    expected_path = Path(db_info.path)
    assert expected_path.exists()
    assert expected_path.is_dir()


def test_db_path_property(temp_dir):
    repo_path = Path(temp_dir)
    db_name = "test_db"
    db_info = DbPath(repo_path, db_name)

    expected_path = repo_path / db_name
    assert db_info.path == expected_path


def test_with_string_path(temp_dir):
    db_name = "string_test_db"
    db_info = DbPath(temp_dir, db_name)

    expected_path = Path(temp_dir) / db_name
    assert db_info.path == expected_path


def test_with_path_object(temp_dir):
    db_name = "path_obj_test_db"
    path_obj = Path(temp_dir)
    db_info = DbPath(path_obj, db_name)

    expected_path = path_obj / db_name
    assert db_info.path == expected_path
