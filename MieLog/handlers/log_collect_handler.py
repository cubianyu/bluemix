__author__ = 'TomasLiu'

import logging

class LogCollectHandler:
  def __init__(self):
    self.log = {}

  def collect(self, logs):
    logging.info("The logs are %s", logs)