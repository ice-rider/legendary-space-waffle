import os
import datetime
import logging


# log format
date_format = "%d.%m.%y %H:%M"
formatter = logging.Formatter("[%(asctime)s] %(name)s -> %(message)s", datefmt=date_format)

logger = logging.getLogger("api_logger")  # take logger
logger.setLevel(logging.DEBUG)


# create folders
if not os.path.exists("logs"):
    os.mkdir("logs")

if not os.path.exists("logs/api"):
    os.mkdir("logs/api")


# set up handlers
date = datetime.datetime.now().strftime("%Y.%m.%d")

console_handler = logging.StreamHandler()  # console logger
file_handler = logging.FileHandler("logs/api/%s.log" % (date,))  # file logger

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.ERROR)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("loggers successfully initialized")
