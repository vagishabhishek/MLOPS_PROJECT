# tests/logger/test_logger.py

import logging
from mlops_project.logger import get_logger
from pathlib import Path
import time
from logging.handlers import RotatingFileHandler


def test_get_logger_returns_logger():
    """
        Test if logger returns a correct logger instance
    """
    log = get_logger("test_module")
    assert log is not None
    assert isinstance(log, logging.Logger)


def test_logger_has_handlers():
    """
        Test if logger has handlers attached to it
    """
    log = get_logger("test_module")
    # Either logger or root logger must have handlers
    assert len(log.handlers) > 0 or len(logging.getLogger().handlers) > 0


def test_logger_level():
    """
        Check for logging level of the logger
        1. Test for predefinitely set level of the logger = logging.DEBUG
        2. Set a new log level and test if it was correctly set
    """

    log = get_logger("test_module")

    #Test 1
    # Either logger inherits NOTSET or root is DEBUG
    assert log.level in (logging.NOTSET, logging.DEBUG)
    
    #Test 2
    #set a new log level
    log.setLevel(logging.INFO)
    assert log.level == logging.INFO



def test_logger_output(caplog):
    """
        Test for logger output, using caplog feature of pytest.
    """
    log = get_logger("test_module")

    #log a message with capture-log level set to logging.DEBUG 
    with caplog.at_level(logging.DEBUG):
        log.info("test message")
    
    #Test if the message was correctly logged
    assert "test message" in (record.message for record in caplog.records)


def test_logger_format():
    log = get_logger("format_tester")

    #import StringIO to test string contents written to stream by logger
    #StringIO is an in-memory-buffer that can be reaf from or written to 
    from io import StringIO
    stream = StringIO()

    # sample formatter for tests
    test_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # temp handler
    temp_handler = logging.StreamHandler(stream)
    temp_handler.setFormatter(test_formatter)
    log.addHandler(temp_handler)

    log.debug("format test")
    temp_handler.flush()

    #get value written to stream
    output = stream.getvalue()

    #check for desired message in stream
    assert "|" in output
    assert "format test" in output

    #cleanup
    log.removeHandler(temp_handler)


def test_logger_file_created(tmp_path):
    """
    Test using a RotatingFileHandler since real logger uses it.
    """
    #create a temporary log file using pytest, written to temp location tmp_path
    temp_log_file = tmp_path / "test_rotating.log"

    logger = get_logger("RotatingTestLogger")

    # Create a **RotatingFileHandler**
    rotating_handler = RotatingFileHandler(
        temp_log_file,
        maxBytes=10_000,
        backupCount=1,
        encoding="utf-8",
        mode="w"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    rotating_handler.setFormatter(formatter)

    # Attach rotating handler
    logger.addHandler(rotating_handler)

    logger.info("Rotating handler test message")
    rotating_handler.flush()#flush and wait as logs may not get written immidietaly
    time.sleep(0.05)

    content = temp_log_file.read_text(encoding="utf-8")
    assert "Rotating handler test message" in content

    # Cleanup
    logger.removeHandler(rotating_handler)
