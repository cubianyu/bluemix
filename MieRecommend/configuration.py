__author__ = 'TomasLiu'

import logging
import os

env = {}
try:
    env = eval(os.getenv('VCAP_SERVICES', "{}"))
    logging.info("The env is %s", env)
except:
    logging.exception("Failed to get the configuration")
