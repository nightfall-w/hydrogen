# -*- coding:utf-8 -*-
import time

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from Logger import logger


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class ElasticsearchClient:

    def __init__(self, es_info):
        self.__dict__.update(es_info)
        self.es_conn = self.connect_elasticsearch()

    def connect_elasticsearch(self):
        es_conn = Elasticsearch([{'host': self.host, 'port': self.port}])
        if es_conn.ping():
            logger.info('ElasticSearch:{} Connect Success.'.format(self.host))
            return es_conn
        else:
            logger.error('ElasticSearch:{} Connect Failed.'.format(self.host))
            raise ConnectionError

    def store_record(self, record, index_name=None, index_type=None):
        index_name = index_name if index_name else self.index_name
        index_type = index_type if index_type else self.index_type
        try:
            outcome = self.es_conn.index(index=index_name, doc_type=index_type, body=record)
            return outcome
        except Exception as ex:
            logger.error('Error in indexing data: {}'.format(record))
            logger.error(str(ex))

    def parse_mq_msg(self, msg):
        logger.info("received message: {}".format(msg))
        data = msg
        try:
            data = eval(msg.body.decode('utf-8'))["event"]
            data["receiveDate"] = int(round(time.time() * 1000))
        except Exception as e:
            logger.error(str(e))
        finally:
            self.store_record(data)

    def create_index(self):
        # index_name的创建相当于mysql的数据库   index_type相当于数据表
        print(self.index_name)
        result = self.es_conn.indices.create(index=self.index_name, ignore=400)
        logger.debug(result)
        if all([self.index_type, self.mapping_config]):
            self.es_conn.indices.put_mapping(index=self.index_name, doc_type=self.index_type, body=self.mapping_config)
        return self.index_name

    def search_by_match(self, index_name, query_dict):
        query = {
            "query": {
                "match": query_dict
            }
        }
        result = self.es_conn.search(index=index_name, body=query)
        return result["hits"]["hits"]

    def search_by_terms(self, index_name, query_dict):
        query = {
            "query": {
                "terms": query_dict
            }
        }
        result = self.es_conn.search(index=index_name, body=query)
        return result["hits"]["hits"]

    def search_by_regexp(self, index_name, query_dict):
        query = {
            "query": {
                "regexp": query_dict
            }
        }
        result = self.es_conn.search(index=index_name, body=query)
        return result["hits"]["hits"]
