#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import logging.handlers


def create_logger():
    """创建日志"""
    #  logger = app.logger
    logger = logging.getLogger('tmdfood')
    logger.setLevel(logging.DEBUG)

    fmt = (
        '[%(asctime)s] [%(funcName)s] [%(pathname)s:%(lineno)d] [%(levelname)s] '
        ' %(message)s '
    )
    #  fmt = RequestFormatter(fmt)
    formatter = logging.Formatter(fmt)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    return logger


logger = create_logger()
