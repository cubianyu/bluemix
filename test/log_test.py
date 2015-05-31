__author__ = 'TomasLiu'

import sys

sys.path.append('gen-py')

from mie_log import LogCollectService
from mie_log.ttypes import *

from thrift import Thrift
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol

try:

  # Make socket
  #transport = TSocket.TSocket('mielog.mybluemix.net', 80)
  protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()

  # Buffering is critical. Raw sockets are very slow
  transport = THttpClient.THttpClient("http://mielog.mybluemix.net/")

  # Wrap in a protocol

  protocol =protocol_factory.getProtocol(transport)
  # Create a client to use the protocol encoder
  client = LogCollectService.Client(protocol)

  # Connect!
  transport.open()

  logs = []
  log = mie_log_struct()
  log.business_id = 1
  log.mark = 9.7
  log.type = mie_log_type.RECOMMEND
  logs.append(log)

  log.business_id = 2
  log.mark = 0
  log.type = mie_log_type.REJECT
  logs.append(log)

  print client.collect(logs)

  # Close!
  transport.close()

except Thrift.TException, tx:
  print '%s' % (tx.message)