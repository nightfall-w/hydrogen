# -*- coding:utf-8 -*-
import json
import time
import uuid
from threading import Thread

from rocketmq.client import Producer, Message
from rocketmq.client import PushConsumer
from Logger import logger


class RocketPushConsumer(Thread):
    def __init__(self, obj):
        super().__init__()
        self.__dict__.update(obj)
        self.group_id = self.group_id
        self.setName("{}:{}-{}-{}".format(self.host, self.port, self.group_id, self.topic))

    def run(self) -> None:
        self.start_consumer()

    def start_consumer(self):
        logger.debug("创建RocketMQ Consumer connect: {}:{}--{}".format(self.host, self.port, self.group_id))
        self.consumer = PushConsumer(self.group_id)
        self.consumer.set_instance_name(str(uuid.uuid4()))
        logger.debug("connecting RocketMQ {}:{}".format(self.host, self.port))
        self.consumer.set_namesrv_addr("{}:{}".format(self.host, self.port))
        self.consumer.subscribe(topic=self.topic, callback=self.es_instance.parse_mq_msg)
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
        send_result = self.producer.send_sync(msg)
        logger.debug(send_result)

    def shutdown(self):
        self.producer.shutdown()
