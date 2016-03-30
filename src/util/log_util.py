#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import glob
import logging
import os
import sys
import traceback


def init_logging(script_dir, date_str, log_level):
    os.makedirs(r'{0}\logs'.format(script_dir), exist_ok=True)
    # fmt = '%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s'

    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    file_name = r'{0}\logs\util {1}.log'.format(script_dir, date_str)
    logging.basicConfig(level=log_level, format=fmt, filename=file_name, filemode='w')


def clean_log_files(script_dir, keep_log_file=10):
    file_list = sorted(glob.glob(r'{0}\logs\*.log'.format(script_dir)), key=os.path.getmtime, reverse=True)

    for i in range(keep_log_file, len(file_list)):
        try:
            os.remove(file_list[i])
        except (IOError, OSError) as e:
            print("Error {}".format(e.args[0]))
        except Exception as e:
            print("Error {}".format(e.args[0]))


def log_information(level, module_name, info_str, line_no=0, message_str=''):
    header = '-' * 50

    if level.upper() == 'INFO':
        logging.info(header)
        logging.info('{0} : {1} - {2}'.format(module_name, line_no, info_str))

        if message_str:
            logging.info('{0} : {1} - {2}'.format(module_name, line_no, message_str))

    if level.upper() == 'ERROR':
        exc_type, exc_value, exc_traceback = sys.exc_info()
        line_no = exc_traceback.tb_lineno
        msg = traceback.format_exc().splitlines()

        logging.error(header)
        logging.error('{0} : {1} - {2}'.format(module_name, line_no, info_str))
        logging.error('{0} : {1} - {2}'.format(module_name, line_no, message_str))

        for line in msg:
            logging.error('{0} : {1}'.format(module_name, line))
