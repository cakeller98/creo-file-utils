#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import logging
import os
import sys
import traceback


def initLogging(scriptDir, dateStr, logLevel):
    os.makedirs(r'{0}\logs'.format(scriptDir), exist_ok=True)
    # fmt = '%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s'

    fmt = '%(asctime)s - %(message)s'
    filename = r'{0}\logs\log {1}.log'.format(scriptDir, dateStr)
    logging.basicConfig(level=logLevel, format=fmt, filename=filename, filemode='w')


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
