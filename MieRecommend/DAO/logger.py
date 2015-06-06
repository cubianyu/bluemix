__author__ = 'TomasLiu'

import time
import pika, os, urlparse, logging
from MieLog.ttypes import Log, LogType

RECOMMEND = 0

class Logger(object):
    @classmethod
    def to_logs(cls, businesses):
        logs = []
        for busi in businesses:
            log = Log(busi.id, LogType.RECOMMEND, timestamp=time.time())
            logs.append(log)
        return logs

    @classmethod
    def append_to_queue(logs):
        pass
