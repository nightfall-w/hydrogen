from threading import Thread

from fastapi import FastAPI
from pydantic.main import BaseModel

from Logger import logger
from utils.config import config
from utils.es_client import ElasticsearchClient
from utils.mq_client import RocketPushConsumer

app = FastAPI()


class EsIndex(BaseModel):
    index_name: str = None
    type_name: str = None
    mapping: dict = {}


@app.get('/')
async def index():
    return {'message': '你已经正确创建 FastApi 服务！'}


@app.post('/api/es/index')
async def es_index(request_data: EsIndex):
    index_name = request_data.index_name
    type_name = request_data.type_name
    mapping = request_data.mapping

    if not index_name:
        return {"success": False, "message": "idnex_name is requirement"}

    es = ElasticsearchClient({"host": config.HOST_IP1, "port": 9200})
    try:
        result = es.create_index(index_name, type_name, mapping)
        return {"success": True, "message": "index_name: {} created success.".format(result)}
    except Exception as e:
        logger.error(str(e))
        logger.error("index :{} create failed.".format(index_name))
        return {"success": False, "message": "index_name: {} created failed.".format(index_name)}


def start_consumer():
    es = ElasticsearchClient(
        {"host": config.HOST_IP1, "port": 9200, "index_name": config.ES_INDEX, "index_type": config.ES_TYPE})
    es.create_index(config.ES_INDEX, config.ES_TYPE, config.mapping)
    rocket_consumer = RocketPushConsumer({"host": config.HOST_IP, "port": 9876, "topic": config.TOPIC})
    rocket_consumer.start(es)


@app.on_event("startup")
def mq_consumer():
    t = Thread(target=start_consumer)
    t.setDaemon(True)
    t.start()
    # t.join()
