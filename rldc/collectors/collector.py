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
        raise Exception

    def publish_stats(self, hosts=['127.0.0.1:9200'], index=None):
        stats = self.get_stats()

        if stats is not None:
            es = Elasticsearch(hosts=hosts)

            meta = {
                'timestamp': datetime.now(),
            }

            doc = dict(stats.items() + meta.items())
            es.create(doc_type=self.type, body=doc, index=index)

if __name__ == '__main__':
    main()
