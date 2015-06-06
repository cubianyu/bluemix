import os
import logging
import time
import threading
from mqutils import MQService, MQUtil
from configuration import env

from thrift.server import THttpServer
from thrift.protocol import TBinaryProtocol

from recommend_controller import RecommendController

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../logs/mie_recommend.log',
                filemode='a')

url = None
try:
  url = env["cloudamqp"][0]["credentials"]["uri"]
  MQUtil = MQService(url, "mie_log")
except:
  logging.exception("Failed to get connection url")


def run():
    while 1:
        MQUtil.post("Hello world")
        logging.info("Sending hello world")

        time.sleep(10)

def run_thrift_server():
    logging.info("run_thrift_server begin")
    try:
        from MieRecommend import RecommendService

        handler = RecommendController()
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

thread = threading.Thread(target = run)
thread.daemon = True
thread.start()
logging.info("Starting the thread")

run_thrift_server()
