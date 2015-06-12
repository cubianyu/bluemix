__author__ = 'TomasLiu'

import logging
import os

env = {}
'''
env = {
  "rediscloud": [
    {
      "name": "Redis Cloud-gn",
      "label": "rediscloud",
      "plan": "25mb",
      "credentials": {
        "hostname": "pub-redis-15138.dal-05.1.sl.garantiadata.com",
        "password": "Xrm9AB0pv9XlQpEK",
        "port": "15138"
      }
    }
  ]
}
'''
try:
    env = eval(os.getenv('VCAP_SERVICES', "{}"))
    env.update(eval(os.getenv('USER_CONFIG', "{}")))
    logging.info("The env is %s", env)
except:
    logging.exception("Failed to get the configuration")
