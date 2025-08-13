import logging

import pymongo
from itemadapter import ItemAdapter

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        # 连接 MongoDB
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 关闭连接
        self.client.close()

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        self.db[self.mongo_collection].update_one(
            {
                "jsondatas.indexdata.id": data['jsondatas']['indexdata']['id'],
                "jsondatas.c_class": data['jsondatas']['c_class']
            },
            {"$set": data},
            upsert=True
        )
        logging.log(logging.INFO,data)
        return item
