__author__ = 'TomasLiu'

import sys

sys.path.append('gen-py')

from MieLog import LogCollectService
from MieLog.ttypes import *

from thrift import Thrift
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol

while 1:
  try:

    # Make socket
    #transport = TSocket.TSocket('mielog.mybluemix.net', 80)
    protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()

    # Buffering is critical. Raw sockets are very slow
    transport = THttpClient.THttpClient("http://mielog.mybluemix.net/")
    #"http://mielog.mybluemix.net/")

    # Wrap in a protocol

    protocol =protocol_factory.getProtocol(transport)
    # Create a client to use the protocol encoder
    client = LogCollectService.Client(protocol)

    '''
         TTransport transport = new THttpClient("http://mielog.mybluemix.net/");
        TProtocol protocol = new  TBinaryProtocol(transport);

        LogCollectService.Client client = new LogCollectService.Client(protocol);
    '''
    # Connect!
    transport.open()

    logs = []
    log = Log()
    log.business_id = 1
    log.mark = 9.7
    log.type = LogType.RECOMMEND
    logs.append(log)

    log.business_id = 2
    log.mark = 0
    log.type = LogType.REJECT
    logs.append(log)

    print client.collect(logs)
    import time
    time.sleep(5)

    # Close!
    transport.close()

  except Thrift.TException, tx:
    print '%s' % (tx.message)