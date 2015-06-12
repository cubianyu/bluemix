import os
import logging
import threading
import sys

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../logs/mie_log.log',
                filemode='a')

from thrift.server import THttpServer
from thrift.protocol import TBinaryProtocol
from configuration import env
from mqutils import MQService, MQUtil

url = None
try:
  url = env["cloudamqp"][0]["credentials"]["uri"]
  MQUtil = MQService(url, "mie_log")
except:
  logging.exception("Failed to get connection url")
  url = "amqp://uksblpna:rEvL8q5O78wbV91jbj4JMFuVFtW1wfZM@white-swan.rmq.cloudamqp.com/uksblpna"
  MQUtil = MQService(url, "mie_log")

from handlers.log_collect_handler import LogCollectHandler
handler = LogCollectHandler()

def run_thrift_server():
    logging.info("run_thrift_server begin")
    try:
        from handlers.log_collect_handler import LogCollectHandler
        from MieLog import LogCollectService

        processor = LogCollectService.Processor(handler)
        port = int(os.getenv('VCAP_APP_PORT', 8001))
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

def on_event(ch, method, properties, body):
    logging.info("%s %s %s %s", ch, method, properties, body)
    try:
        logs = eval(body)
        handler.collect(logs)
    except:
        logging.exception("Failed to eval body")

print "***************"
MQUtil.consume(on_event)
print "***************"

run_thrift_server()