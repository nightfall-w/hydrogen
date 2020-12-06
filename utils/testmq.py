# -*- coding:utf-8 -*-
import random
import time

from utils.config import config
from utils.es_client import ElasticsearchClient
from utils.mq_client import RocketProducer, RocketPushConsumer

rocket_producer = RocketProducer({"host": "172.31.236.21", "port": 9876})
rocket_producer.start()
for i in range(10):
    data = {
        "id": random.randint(1, 10000),
        "trance_id": random.randint(1, 1000),
        "order_id": random.randint(1, 1000),
        "biz_job_id": "aaaa",
        "transfer_job_id": "bbbb",
        "move_job_id": "cccc",
        "agv_code": "dddd",
        "container_code": 9001001002,
        "log_level": "ERROR",
        "message": "abcdefg222222222222222",
        "created_time": int(round(time.time() * 1000)),
        "created_app": "wcs"
    }
    rocket_producer.push("log", data)
rocket_producer.shutdown()

# rocket_consumer = RocketPushConsumer({"host": "172.31.236.21", "port": 9876, "topic": "log"})
# es_instance = ElasticsearchClient(
#     {"host": config.HOST_IP1, "port": 9200, "index_name": config.ES_INDEX, "index_type": config.ES_TYPE})
# rocket_consumer.start(es_instance)
# from utils.config import config
# from utils.es_client import ElasticsearchClient
#
# es1 = ElasticsearchClient(
#     {"host": config.HOST_IP1, "port": 9200, "index_name": config.ES_INDEX, "index_type": config.ES_TYPE})
# print(es1)
# es2 = ElasticsearchClient(
#     {"host": config.HOST_IP1, "port": 9200, "index_name": config.ES_INDEX, "index_type": config.ES_TYPE})
# print(es2)
# print(id(es1))
# print(id(es2))
