
_error_log_file = "error.log"


def add_error(string_to_write):
    error_file_ptr = open(_error_log_file, "a")
    error_file_ptr.write(string_to_write + "\n")
    error_file_ptr.close()
