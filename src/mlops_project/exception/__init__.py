import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error information including files, line number, error message.

    Args:
        error (Exception): The Exception that occurred
        error_detail (sys): Sys module to extract traceback details

    Returns:
        str: A formatted error message string
    """
    # Get the current exception info
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is not None:
        # Extract filename and line number from traceback
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in python script : |{file_name}| at line number |{line_number}|: {str(error)}"
    else:
        # Fallback when no traceback exists (e.g., manually raised exceptions)
        error_message = f"Error: {str(error)}"

    logging.error(error_message)
    return error_message


class MyException(Exception):
    """
    Custom Exception class for handling errors in the app.
    """

    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes the Exception class with a detailed error message.

        Args:
            error_message (str): Description of error
            error_detail (sys): sys module object to get traceback details
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
