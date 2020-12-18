import os


class Config:
    ES_HOST = os.getenv('es_host')
    ES_PORT = os.getenv('es_port', 9200)
    MQ_HOST = os.getenv('mq_host')
    MQ_PORT = int(os.getenv('mq_port', 9876))
    MQ_GROUP = os.getenv('mq_group', 'LogResolver')
    TOPIC = os.getenv("topic", "w2pLog")
    ES_INDEX = os.getenv("es_index", "w2p_log")
    ES_TYPE = os.getenv("es_type", "link")
    mapping = {
        "properties": {
            "tranceId": {"type": "integer"},
            "bizJobId": {"type": "text"},
            "transferJobId": {"type": "text"},
            "moveJobId": {"type": "text"},
            "agvCode": {"type": "text"},
            "containerCode": {"type": "text"},
            "logLevel": {"type": "text"},
            "message": {"type": "text"},
            "state": {"type": "text"},
            "createdTime": {
                "type": "date",
                "format": "strict_date_optional_time||epoch_millis||yyyy-MM-dd HH:mm:ss.SSS"
            },
            "createdApp": {"type": "text"},
            "receiveDate": {
                "type": "date",
                "format": "strict_date_optional_time||epoch_millis||yyyy-MM-dd HH:mm:ss.SSS"
            }
        }
    }


config = Config()
