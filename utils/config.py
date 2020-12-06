import os


class Config:
    HOST_IP = os.getenv('host_ip')
    HOST_IP = "172.31.236.21"
    HOST_IP1 = "127.0.0.1"
    TOPIC = os.getenv("topic", "log")
    ES_INDEX = os.getenv("es_index", "log")
    ES_TYPE = os.getenv("es_type", "link")
    mapping = {
        "properties": {
            "id": {"type": "long"},
            "trance_id": {"type": "long"},
            "order_id": {"type": "long"},
            "biz_job_id": {"type": "text"},
            "transfer_job_id": {"type": "text"},
            "move_job_id": {"type": "text"},
            "agv_code": {"type": "text"},
            "container_code": {"type": "long"},
            "log_level": {"type": "text"},
            "message": {"type": "text"},
            "created_time": {
                "type": "date",
                "format": "strict_date_optional_time||epoch_millis||yyyy-MM-dd HH:mm:ss.SSS"
            },
            "created_app": {"type": "text"},
            "receive_date": {
                "type": "date",
                "format": "strict_date_optional_time||epoch_millis||yyyy-MM-dd HH:mm:ss.SSS"
            }
        }
    }


config = Config()
