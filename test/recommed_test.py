__author__ = 'TomasLiu'
from MieRecommend import RecommendService
from MieRecommend.ttypes import *

from thrift import Thrift
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol

while 1:
  try:

    # Make socket
    #transport = TSocket.TSocket('mielog.mybluemix.net', 80)
    protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()

    # Buffering is critical. Raw sockets are very slow
    transport = THttpClient.THttpClient("http://mierecommend.mybluemix.net/")
    #"http://mielog.mybluemix.net/")

    # Wrap in a protocol

    protocol =protocol_factory.getProtocol(transport)
    # Create a client to use the protocol encoder
    client = RecommendService.Client(protocol)

    # Connect!
    transport.open()

    geo_info = GeoInfo(city="beijing", district="zhongguancun", longitude=116.306783, latitude=39.984)
    mode = Mode(number=1, type=1, style=(1<<9 -1))
    businesses = client.recommend(1, geo_info, mode)
    print businesses
    # Close!
    transport.close()
    import time
    time.sleep(5)
  except Thrift.TException, tx:
    print '%s' % (tx.message)