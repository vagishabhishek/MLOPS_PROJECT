import sys
from mlops_project.exception import MyExcption
import pandas as pd
import pytest

def test_custom_exception1():
    try:
        1 / 0
    except Exception as e:
        exc = MyExcption(str(e), sys)

    # assertions
    msg = str(exc)
    assert "division by zero" in msg
    assert ".py" in msg
    assert "line number" in msg

def test_custom_exception2():
    try :
        df = pd.read_csv("MyFile.csv")
    
    except Exception as e:
        exc = MyExcption(str(e),sys)

    msg = str(exc)
    assert "No such file or directory" in msg
    assert ".py" in msg
    assert "line number" in msg