import os
import logging
import threading
import sys

from thrift.server import THttpServer
from thrift.protocol import TBinaryProtocol

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../logs/mie_log.log',
                filemode='a')

def run_thrift_server():
    logging.info("run_thrift_server begin")
    try:
        from handlers.log_collect_handler import LogCollectHandler
        from mie_log import LogCollectService

        handler = LogCollectHandler()
        processor = LogCollectService.Processor(handler)
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

run_thrift_server()

'''
try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

# Read port selected by the cloud for our application
PORT = int(os.getenv('VCAP_APP_PORT', 8000))
# Change current directory to avoid exposure of control files
os.chdir('static')

httpd = Server(("", PORT), Handler)
thread = threading.Thread(target = run_thrift_server)
thread.daemon = True

try:
  logging.info("Start serving at port %i" % PORT)
  thread.start()
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()
'''