"""
File for config logger
"""
import logging

logger = logging.getLogger('blktest_logger')
logger.setLevel(logging.DEBUG)

# set format for logger
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create handler for debug and higher messages
file_handler_info = logging.FileHandler('logs/blktest.log')
file_handler_info.setLevel(logging.INFO)
file_handler_info.setFormatter(log_formatter)

file_handler_debug = logging.FileHandler('logs/blktest_debug.log')
file_handler_debug.setLevel(logging.DEBUG)
file_handler_debug.setFormatter(log_formatter)

# add handlers to logger
logger.addHandler(file_handler_info)
logger.addHandler(file_handler_debug)
