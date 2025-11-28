import sys
import logging

def error_message_detail(error:Exception,error_detail:sys)->str:
    """
    Extracts detailed error information including files, line number, error message.

    Args:
        error (Exception): The Esception that occurred
        error_detail (sys): Sys object to extract error details

    Returns:
        str: A formatted error message string.
    """

    #Extract traceback details (exception information)

    #1. Get traceback of the error
    _,_,exc_tb = error_detail.exc_info()

    #2. Get the file name from exception_tracback ->traceback_frame->f_code-
    file_name = exc_tb.tb_frame.f_code.co_filename


    #Create a formatted error message string with filename,line number,and the actual error
    line_number = exc_tb.tb_lineno
    error_message = f'Error occurred in python script : |{file_name}| at line number |{line_number}|: {str(error)}'

    # Log the error for better tracking 
    logging.error(error_message)

    return error_message

class MyExcption(Exception):
    """
    Custom Exception class for handling errors in the app
    """

    def __init__(self, error_message:str, error_detail:sys):
        """Initializes the Exception class with a detailed error message

        Args:
            error_message (str): Description of error
            error_detail (sys): sys module object to get tracback details
        """
        # Call Exception Base class constructor with the error message
        super().__init__(error_message)

        # Format the detailed error message using the error_message_detail() function
        self.error_message = error_message_detail(error_message,error_detail)

    def __str__(self):
        """
        Returns the string representation of the error message
        """
        return self.error_message
