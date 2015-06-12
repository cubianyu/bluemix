import os
import logging
import time
import threading

from thrift.server import THttpServer
from thrift.protocol import TBinaryProtocol

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../logs/mie_recommend.log',
                filemode='a')

from configuration import env
from mqutils import MQService
from recommend_controller import RecommendController

mqutil = None
try:
  url = env["cloudamqp"][0]["credentials"]["uri"]
  mqutil = MQService(url, "mie_log")
except:
  logging.exception("Failed to get connection url")
  url = "amqp://hvvpgyfu:04sv5IU9VVY_S55Cpk4ZB1dLYVB7G31O@white-swan.rmq.cloudamqp.com/hvvpgyfu"
  mqutil = MQService(url, "mie_log")

from dbutils import DB
dbutil = None
try:
  redis_creds = env['rediscloud'][0]['credentials']
  dbutil = DB(redis_creds['hostname'], int(redis_creds['port']), redis_creds['password'])
except:
  logging.exception("Failed to get redis host")
  dbutil = DB("pub-redis-15138.dal-05.1.sl.garantiadata.com", 15138, 'Xrm9AB0pv9XlQpEK')

def run_thrift_server():
    logging.info("run_thrift_server begin")
    try:
        from MieRecommend import RecommendService
        from dbutils import DBUtil

        handler = RecommendController(dbutil)
        processor = RecommendService.Processor(handler)
        port = int(os.getenv('VCAP_APP_PORT', 8000))
        logging.info("Using port %s", port)
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        # You could do one of these for a multithreaded server
        #server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
        #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
        #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
        server = THttpServer.THttpServer(processor, ('', port), pfactory)
        server.serve()

        logging.info('Starting the thrift server...')
        server.serve()
        logging.info('done.')
    except:
        logging.exception("Except on starting server")

    logging.info("run_thrift_server stop")

#from DAO.business import Business
#print dbutil
#Business.dump_business(dbutil)
#print "done"
#from DAO.user import User
#User.dump_user(dbutil)
run_thrift_server()
