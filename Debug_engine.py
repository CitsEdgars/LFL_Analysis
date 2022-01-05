import os
import pathlib
from datetime import datetime 

log_dir = "log"

def log_debug(message):
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    log_name = "log_{}.log".format(str(datetime.now().date()).replace("-", ""))
    log_path = str(pathlib.Path().resolve()) + "\\" + log_dir + "\\" 
    file = open(log_path + log_name,'a+')
    now = datetime.now().strftime("%H:%M:%S")
    log_line = "[{}] DEBUG: {}\n".format(now, message)
    file.write(log_line)

def log_error(message):
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    log_name = "log_{}.log".format(str(datetime.now().date()).replace("-", ""))
    log_path = str(pathlib.Path().resolve()) + "\\" + log_dir + "\\" 
    file = open(log_path + log_name,'a+')
    now = datetime.now().strftime("%H:%M:%S")
    log_line = "[{}] ERROR: {}\n".format(now, message)
    file.write(log_line)