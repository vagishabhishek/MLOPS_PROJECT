import pytest
from pathlib import Path
from mlops_project.exception import MyExcption
import mlops_project.utils.mongo_utils as mu  # global import for all tests


# Helper function to write .env file
def write_env(path: Path, content: str):
    """
    Write content to a .env file.
    Ensures parent directories exist before writing.
    """
    path.parent.mkdir(parents=True, exist_ok=True)  # create directories if missing
    path.write_text(content)  # write the .env file


@pytest.fixture
def env_paths(tmp_path):
    """
    Fixture to create temporary paths for testing.
    
    Returns a dictionary with:
    - project_root: base temp folder
    - env_dir: folder where .env will be placed
    - env_file: full path to mongo_cred.env
    """
    project_root = tmp_path / "project"
    env_dir = project_root / ".env"
    env_file = env_dir / "mongo_cred.env"
    return {"project_root": project_root, "env_dir": env_dir, "env_file": env_file}


def test_create_mongo_uri_success(env_paths, monkeypatch):
    """
    Test successful creation of MongoDB URI.
    Writes a complete .env file and asserts the returned URI.
    """
    # Remove any real env vars to isolate test
    for key in ["MONGO_USER", "MONGO_PASSWORD", "MONGO_HOST", "CLUSTER"]:
        monkeypatch.delenv(key, raising=False)

    # Force from_root() to use temp project folder
    monkeypatch.setattr(
        "mlops_project.utils.mongo_utils.from_root",
        lambda: str(env_paths["project_root"])
    )

    # Write a valid test .env file
    write_env(
        env_paths["env_file"],
        "MONGO_USER=testuser\nMONGO_PASSWORD=testpass\nMONGO_HOST=cluster0.mongodb.net\nCLUSTER=TestCluster\n"
    )

    # Generate URI and assert
    uri = mu.create_mongo_uri()
    assert uri == "mongodb+srv://testuser:testpass@cluster0.mongodb.net/?appName=TestCluster"


def test_missing_env_directory(env_paths, monkeypatch):
    """
    Should raise MyExcption when .env folder is missing.
    Folder is NOT created to simulate missing directory.
    """
    for key in ["MONGO_USER", "MONGO_PASSWORD", "MONGO_HOST", "CLUSTER"]:
        monkeypatch.delenv(key, raising=False)

    monkeypatch.setattr(
        "mlops_project.utils.mongo_utils.from_root",
        lambda: str(env_paths["project_root"])
    )

    with pytest.raises(MyExcption):
        mu.create_mongo_uri()


def test_missing_env_file(env_paths, monkeypatch):
    """
    Should raise MyExcption when mongo_cred.env file is missing.
    Folder exists but file is not created.
    """
    for key in ["MONGO_USER", "MONGO_PASSWORD", "MONGO_HOST", "CLUSTER"]:
        monkeypatch.delenv(key, raising=False)

    # Only create folder, not file
    env_paths["env_dir"].mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(
        "mlops_project.utils.mongo_utils.from_root",
        lambda: str(env_paths["project_root"])
    )

    with pytest.raises(MyExcption):
        mu.create_mongo_uri()


def test_missing_env_fields(env_paths, monkeypatch):
    """
    Should raise MyExcption when required environment variables are missing.
    Creates a .env file with missing CLUSTER variable.
    """
    for key in ["MONGO_USER", "MONGO_PASSWORD", "MONGO_HOST", "CLUSTER"]:
        monkeypatch.delenv(key, raising=False)

    monkeypatch.setattr(
        "mlops_project.utils.mongo_utils.from_root",
        lambda: str(env_paths["project_root"])
    )

    # Write incomplete env file (missing CLUSTER)
    write_env(
        env_paths["env_file"],
        "MONGO_USER=testuser\nMONGO_PASSWORD=testpass\nMONGO_HOST=cluster0.mongodb.net\n"
    )

    with pytest.raises(MyExcption):
        mu.create_mongo_uri()
