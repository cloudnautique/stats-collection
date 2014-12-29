from elasticsearch import Elasticsearch
from datetime import datetime

import logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class ElasticsearchDataCollector(object):
    def get_stats(self):
        raise NotImplementedError

    def __prep_publish_blob(self, stats):
        meta = {
            'timestamp': datetime.now(),
        }

        return dict(stats.items() + meta.items())

    def publish_stats(self, stats, hosts=['127.0.0.1:9200'], index=None):
        if stats is not None and isinstance(stats, list):
            es = Elasticsearch(hosts=hosts)

            for stat in stats:
                doc = self.__prep_publish_blob(stat)
                es.create(doc_type=self.type, body=doc, index=index)
