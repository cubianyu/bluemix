__author__ = 'TomasLiu'

import time
import pika, os, urlparse, logging
from MieLog.ttypes import Log, LogType

from mqutils import MQUtil

RECOMMEND = 0

class Logger(object):
    @classmethod
    def to_logs(cls, businesses):
        logs = []
        for busi in businesses:
            log = Log(busi["business_id"], LogType.RECOMMEND, timestamp=time.time())
            logs.append(log)
        return logs

    @classmethod
    def append_to_queue(cls, logs):
        if MQUtil:
            MQUtil.post(logs)
            logging.info("After post event for logs, size is %s", len(logs))
        else:
            logging.error("Failed to post event")
