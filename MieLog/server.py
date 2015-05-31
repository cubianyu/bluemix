import os
import logging
import threading
import sys

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

sys.path.append('gen-py')

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../logs/mie_log.log',
                filemode='a')

try:
    from handlers.log_collect_handler import LogCollectHandler
    from mie_log import LogCollectService

    handler = LogCollectHandler()
    processor = LogCollectService.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # You could do one of these for a multithreaded server
    #server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    logging.info('Starting the thrift server...')
    thread = threading.Thread(target = server.serve)
    thread.daemon = True
    thread.start()
    logging.info('done.')
except:
    logging.exception("Except on starting server")

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
try:
  logging.info("Start serving at port %i" % PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()

