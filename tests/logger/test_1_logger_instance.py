from mlops_project.logger  import get_logger
import logging

def test_get_logger_returns_logger()->None:
    """
        Test if logger returns a proper instance
    """
    try:
        log = get_logger("test module")
        assert isinstance(log,logging.Logger)
        assert log.name == "test_module"
        log.debug("Test 1 passed")
    except Exception as e:
        log.error(f"Logger instance test failed with {e}",exc_info=True)