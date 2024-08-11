import logging
import socket
import dotenv
import os
import config

"""
DESCRIPTION:
    This is a logger module that logs messages to a file and to the console.
    The log messages are formatted as a dictionary.
    The dictionary is then converted to a string and logged.
    The Length of the dictionary is not limited.

FUNCTIONS:
    log_debug : logs a debug message
    log_info : logs an info message
    log_error : logs an error message
    log_warning : logs a warning message
    log_critical : logs a critical message

ENVARS:
    LOG_LEVEL : the log level
    LOG_FILE_NAME : the name of the log file

"""

dotenv.load_dotenv()
ip_address = socket.gethostbyname(socket.gethostname())
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))

format_str = f"""\nDate:%(asctime)s,Ip-Address:{ip_address},Status:%(levelname)s,\n%(message)s"""
format = logging.Formatter(format_str)

#################### file output ####################
log_file_name = config.logger_filename

if not os.path.exists(log_file_name):
    open(log_file_name, 'w').close()
file_handler = logging.FileHandler(log_file_name)
file_handler.setFormatter(format)
logger.addHandler(file_handler)

####################################################
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format)
logger.addHandler(stream_handler)


def log_debug(log_dict: dict):
    if not isinstance(log_dict, dict):
        raise ValueError("log_dict must be a dictionary")
    str_log = "".join([f"{key} : {log_dict[key]}\n" for key in log_dict.keys()])
    logger.debug(str_log)

def log_info(log_dict: dict):
    if not isinstance(log_dict, dict):
        raise ValueError("log_dict must be a dictionary")
    str_log = "".join([f"{key} : {log_dict[key]}\n" for key in log_dict.keys()])
    logger.info(str_log)

def log_error(log_dict: dict):
    if not isinstance(log_dict, dict):
        raise ValueError("log_dict must be a dictionary")
    str_log = "".join([f"{key} : {log_dict[key]}\n" for key in log_dict.keys()])
    logger.error(str_log)

def log_warning(log_dict: dict):
    if not isinstance(log_dict, dict):
        raise ValueError("log_dict must be a dictionary")
    str_log = "".join([f"{key} : {log_dict[key]}\n" for key in log_dict.keys()])
    logger.warning(str_log)

def log_critical(log_dict: dict):
    if not isinstance(log_dict, dict):
        raise ValueError("log_dict must be a dictionary")
    str_log = "".join([f"{key} : {log_dict[key]}\n" for key in log_dict.keys()])
    logger.critical(str_log)

if __name__ == "__main__":
    log_info({"name":"John", "age": 30, "city":"New York"})
    log_debug({"debug":"debug message", "error_code": 500})
    log_error({"error":"error message", "error_code": 404})
    log_warning({"warning":"warning message", "error_code": 300})
    log_critical({"critical":"critical message", "error_code": 700})