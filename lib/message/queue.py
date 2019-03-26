import pika
from lib.config import config

class MsgConnect(object):
    def __init__(self, _queue_name):
        self._queue_name = _queue_name
        user_pwd = pika.PlainCredentials(config.QUEUE_USERNAME, config.QUEUE_PASSWORD)
        self._s_conn = pika.BlockingConnection(pika.ConnectionParameters(config.QUEUE_ADDRESS, credentials=user_pwd))
        self.chan = self._s_conn.channel()
        self.chan.queue_declare(queue=self._queue_name)


class MsgRecv(MsgConnect):
    def __init__(self, _queue_name, _callback):
        super(MsgRecv, self).__init__(_queue_name)
        self.chan.basic_consume(_callback, queue=_queue_name)


class MsgProducer(MsgConnect):
    def send_message(self, message):
        self.chan.basic_publish(exchange='',
                       routing_key=self._queue_name,
                       body=message
                       )
    def close(self):
        self._s_conn.close()