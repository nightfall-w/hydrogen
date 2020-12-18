from fastapi import FastAPI
from pydantic.main import BaseModel

from Logger import logger
from utils.config import config
from utils.es_client import ElasticsearchClient
from utils.mq_client import RocketPushConsumer

app = FastAPI()


class EsIndex(BaseModel):
    es_host: str = config.ES_HOST
    es_port: int = config.ES_PORT
    index_name: str = config.ES_INDEX
    type_name: str = config.ES_TYPE
    mapping: dict = {}


class MqConsumer(BaseModel):
    mq_host: str = config.MQ_HOST
    mq_port: int = config.MQ_PORT
    mq_group: str = config.MQ_GROUP
    mq_topic: str = config.TOPIC


@app.get('/')
async def index():
    return {'message': '你已经正确创建 FastApi 服务！'}


@app.post('/api/es/index')
async def es_index(request_data: EsIndex):
    es_host = request_data.es_host
    es_port = request_data.es_port
    index_name = request_data.index_name
    type_name = request_data.type_name
    mapping_config = request_data.mapping

    if not all([es_host, es_port, index_name, type_name, mapping_config]):
        return {"success": False, "message": "Lack of necessary parameters"}

    es = ElasticsearchClient({"host": es_host, "port": es_port, "index_name": index_name, "type_name": type_name,
                              "config_mapping": mapping_config})
    try:
        result = es.create_index()
        return {"success": True, "message": "index_name: {} created success.".format(result)}
    except Exception as e:
        logger.error(str(e))
        logger.error("index :{} create failed.".format(index_name))
        return {"success": False, "message": "index_name: {} created failed.".format(index_name)}


@app.post('/api/mq/consumer')
async def mq_consumer(request_data: MqConsumer):
    mq_host = request_data.mq_host
    mq_port = request_data.mq_port
    mq_group = request_data.mq_group
    mq_topic = request_data.mq_topic

    if not all([mq_host, mq_port, mq_group, mq_topic]):
        return {"success": False, "message": "Lack of necessary parameters"}
    start_consumer(mq_host, mq_port, mq_topic, mq_group)
    return {"success": True}


def start_consumer(mq_host, mq_port, mq_topic, mq_group=config.MQ_GROUP):
    # create elasticsearch instance
    es = ElasticsearchClient(
        {"host": config.ES_HOST, "port": config.ES_PORT,
         "index_name": mq_host.replace(".", "-") + "-" + config.ES_INDEX,
         "index_type": config.ES_TYPE, "mapping_config": config.mapping})
    # create es index
    es.create_index()

    # create RocketMQ instance
    rocket_consumer = RocketPushConsumer(
        {"host": mq_host, "port": mq_port, "group_id": mq_group, "topic": mq_topic, "es_instance": es})
    rocket_consumer.setDaemon(True)
    rocket_consumer.start()


@app.on_event("startup")
def mq_consumer():
    start_consumer(config.MQ_HOST, config.MQ_PORT, config.TOPIC)
