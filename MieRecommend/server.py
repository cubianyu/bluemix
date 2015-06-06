import os
import logging
import time
import threading
from mqutils import MQUtil

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../logs/mie_log.log',
                filemode='a')
try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

def run():
    while 1:
        MQUtil.post("Hello world")
        logging.info("Sending hello world")

        time.sleep(10)

# Read port selected by the cloud for our application
PORT = int(os.getenv('VCAP_APP_PORT', 8000))

# Change current directory to avoid exposure of control files
os.chdir('static')

thread = threading.Thread(target = run)
thread.daemon = True
thread.start()
logging.info("Starting the thread")

httpd = Server(("", PORT), Handler)
try:
  logging.info("Start serving at port %i", PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()


