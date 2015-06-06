__author__ = 'TomasLiu'

import logging
import pika, os, urlparse, logging

from configuration import env

'''
{
  "cloudamqp": [
    {
      "name": "CloudAMQP-fa",
      "label": "cloudamqp",
      "plan": "lemur",
      "credentials": {
        "uri": "amqp://uksblpna:rEvL8q5O78wbV91jbj4JMFuVFtW1wfZM@white-swan.rmq.cloudamqp.com/uksblpna",
        "http_api_uri": "https://uksblpna:rEvL8q5O78wbV91jbj4JMFuVFtW1wfZM@white-swan.rmq.cloudamqp.com/api/"
      }
    }
  ]
}
'''

# Parse CLODUAMQP_URL (fallback to localhost)

MQUtil = None

class MQService(object):
  def __init__(self, url, queue):
    self.__url = url
    self.__queue = queue
    params = pika.URLParameters(self.__url)
    params.socket_timeout = 5
    self.__connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    self.__channel = self.__connection.channel() # start a channel
    self.__channel.queue_declare(queue=self.__queue) # Declare a queue

  def __del__(self):
    if self.__connection:
      self.__connection.close()

  def post(self, event):
    self.__channel.basic_publish(exchange='', routing_key=self.__queue, body=str(event))

  def consume(self, callback):
    self.__channel.basic_consume(callback, queue=self.__queue, no_ack=True)
    self.__channel.start_consuming()