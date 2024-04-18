import sys


def error_message_details(error, error_detail: sys):
    _, _, exception_tb = error_detail.exc_info()

    file_name = exception_tb.tb_frame.f_code.co_filename

    error_msg = f"Error occured in file : {file_name} at line : {exception_tb.tb_lineno} & error message : {str(error)}"
    return error_msg


class sensor_exception(Exception):
    def __init__(self, error_msg, error_detail : sys):
        super().__init__(error_msg)

        self.error_msg = error_message_details(error = error_msg, error_detail = error_detail)
    
    def __str__(self):
        return self.error_msg