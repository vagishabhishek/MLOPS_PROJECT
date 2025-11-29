import os
import pytest
from mlops_project.utils.mongo_utils import create_mongo_uri
from mlops_project.exception import MyException

# ---------------------- TEST: SUCCESS ----------------------
def test_create_mongo_uri_success(monkeypatch):
    """
    Test successful creation of MongoDB URI when all required environment variables are set.

    Steps:
        - Set MONGO_USER, MONGO_PASSWORD, MONGO_HOST, and CLUSTER.
        - Call create_mongo_uri().
        - Validate that the returned URI contains all credentials correctly.
    """
    monkeypatch.setenv("MONGO_USER", "testuser")
    monkeypatch.setenv("MONGO_PASSWORD", "testpass")
    monkeypatch.setenv("MONGO_HOST", "cluster0.mongodb.net")
    monkeypatch.setenv("CLUSTER", "TestCluster")

    uri = create_mongo_uri()
    assert uri.startswith("mongodb+srv://")
    assert "testuser" in uri
    assert "testpass" in uri
    assert "cluster0.mongodb.net" in uri
    assert "TestCluster" in uri

# ---------------------- TEST: MISSING SINGLE VARIABLE ----------------------
def test_missing_single_env_var(monkeypatch):
    """
    Test that MyException is raised when one required environment variable is missing.

    Steps:
        - Set all required variables except CLUSTER.
        - Call create_mongo_uri().
        - Expect MyException with a message indicating the missing variable.
    """
    monkeypatch.setenv("MONGO_USER", "testuser")
    monkeypatch.setenv("MONGO_PASSWORD", "testpass")
    monkeypatch.setenv("MONGO_HOST", "cluster0.mongodb.net")
    monkeypatch.delenv("CLUSTER", raising=False)

    with pytest.raises(MyException) as exc:
        create_mongo_uri()
    assert "Missing required environment variables" in str(exc.value)

# ---------------------- TEST: MISSING MULTIPLE VARIABLES ----------------------
def test_missing_multiple_env_vars(monkeypatch):
    """
    Test that MyException is raised when multiple environment variables are missing.

    Steps:
        - Set only MONGO_USER.
        - Leave MONGO_PASSWORD, MONGO_HOST, and CLUSTER unset.
        - Call create_mongo_uri().
        - Expect MyException indicating all missing variables.
    """
    monkeypatch.setenv("MONGO_USER", "testuser")
    monkeypatch.delenv("MONGO_PASSWORD", raising=False)
    monkeypatch.delenv("MONGO_HOST", raising=False)
    monkeypatch.delenv("CLUSTER", raising=False)

    with pytest.raises(MyException) as exc:
        create_mongo_uri()
    assert "Missing required environment variables" in str(exc.value)

# ---------------------- TEST: SPECIAL CHARACTERS ENCODING ----------------------
def test_mongo_credentials_encoding(monkeypatch):
    """
    Test that special characters in user and password are URL-encoded correctly.

    Steps:
        - Set MONGO_USER and MONGO_PASSWORD with special characters (+, @, /).
        - Set remaining variables normally.
        - Call create_mongo_uri().
        - Verify that special characters are percent-encoded in the URI.
    """
    monkeypatch.setenv("MONGO_USER", "user+name")
    monkeypatch.setenv("MONGO_PASSWORD", "p@ss/word")
    monkeypatch.setenv("MONGO_HOST", "cluster0.mongodb.net")
    monkeypatch.setenv("CLUSTER", "TestCluster")

    uri = create_mongo_uri()
    assert "user%2Bname" in uri
    assert "p%40ss%2Fword" in uri
