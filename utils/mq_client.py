# -*- coding:utf-8 -*-
import json
import time

from rocketmq.client import Producer, Message
from rocketmq.client import PushConsumer

from Logger import logger
from utils.config import config
from utils.es_client import ElasticsearchClient


def callback(msg):
    print(msg)
    data = eval(msg.body.decode('utf-8'))
    data["receive_date"] = int(round(time.time() * 1000))
    es = ElasticsearchClient(
        {"host": config.HOST_IP1, "port": 9200, "index_name": config.ES_INDEX, "index_type": config.ES_TYPE})
    es.store_record(data)


class RocketPushConsumer:
    def __init__(self, obj):
        self.group_id = "LogResolver"
        self.__dict__.update(obj)

    def start(self, es_instance):
        self.consumer = PushConsumer(self.group_id)
        self.consumer.set_namesrv_addr("{}:{}".format(self.host, self.port))
        self.consumer.subscribe(topic=self.topic, callback=es_instance.parse_mq_msg)
        self.consumer.start()
        logger.info("RocketMQ Consumer started.")

        while True:
            time.sleep(3600)
        self.consumer.shutdown()


class RocketProducer:
    def __init__(self, obj):
        self.group_id = "default"
        self.__dict__.update(obj)

    def start(self):
        self.producer = Producer(self.group_id)
        self.producer.set_namesrv_addr('{}:{}'.format(self.host, self.port))  # rocketmq队列接口地址（服务器ip:port）
        self.producer.start()

    def push(self, topic, msg_body):
        msg = Message(topic)
        msg.set_body(json.dumps(msg_body).encode('utf-8'))
        self.producer.send_sync(msg)
        # print(retmq.status, retmq.msg_id, retmq.offset)

    def shutdown(self):
        self.producer.shutdown()
