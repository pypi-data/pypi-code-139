
import pymongo
from pymongo import MongoClient

class mongoUtil:

    def OpenDB(self, dbname):
        uri = "mongodb://home.hddly.cn:57017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
        # uri = "mongodb://10。255。10。52:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
        self.con = MongoClient(uri, connect=False)
        self.db = self.con[dbname]
        # self.collection = self.db[collection]

    def closeDB(self):
        self.con.close()

    def process_item(self, item, collection):
        jsontmp = dict(item)
        self.collection = self.db[collection]
        self.collection.insert_one(jsontmp)
        return item

    def process_items(self, items, collection):
        docs = []
        for item in items:
            jsontmp = dict(item)
            docs.append(jsontmp)
        if len(docs) > 0:
            self.collection = self.db[collection]
            self.collection.insert_many(docs)
        return items

    def get_db_count(self, collection, collector):
        self.collection = self.db[collection]
        rowcount = self.collection.count_documents({'collector': collector})
        return {'collector': collector, 'collcount': rowcount}

    def get_db_count_all(self, collection):
        self.collection = self.db[collection]
        cur = self.collection.aggregate([
            {"$group": {"_id": "$collector", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ])
        # $group操作符去利用一个指定的键进行分组
        # $collector - key
        # $sum累加器进行文档的统计计算
        # $sort 排序
        counts = dict()
        for document in cur:
            # print(document)
            counts[document['_id']] = document['count']
            if document['_id'] and document['count']:
                print(document['_id'] + '\t' + str(document['count']))
        return counts

    def set_db_index(self):
        self.db['users'].create_index([('id', pymongo.ASCENDING)])
        self.db['weibos'].create_index([('id', pymongo.ASCENDING)])

    def insertMongdbOne(self,collection, jsoninfo):
        self.collection = self.db[collection]
        print(jsoninfo)
        self.collection.insert_one(jsoninfo)

if __name__ == '__main__':

    mongo = mongoUtil()
    mongo.OpenDB("pythondb")

    mongo.closeDB()
    exit()
