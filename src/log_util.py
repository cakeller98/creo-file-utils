#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import logging
import os


def initLogging(scriptDir, dateStr, logLevel):
    os.makedirs(r'{0}\logs'.format(scriptDir), exist_ok=True)
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s'
    filename = r'{0}\logs\log {1}.log'.format(scriptDir, dateStr)
    logging.basicConfig(level=logLevel, format=fmt, filename=filename, filemode='w')


def log_information(level, module_name, line_no, info_str='', message_str=''):
    header = '---------------------------------'

    if level.upper() == 'ERROR':
        logging.error(header)
        logging.error('{0} : {1} - {2}'.format(module_name, line_no, info_str))
        logging.error('{0} : {1} - {2}'.format(module_name, line_no, message_str))
