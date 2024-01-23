from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        mongoUrl = "mongodb://localhost:27017"
        self.client = MongoClient(mongoUrl)
        self.db = self.client.local
        self.collection = self.db['jobs']
        self.comps = self.db['comps']
        print(self.collection)

    def insertList(self, list):
        result = self.collection.insert_many(list, ordered=False)
    def insertOne(self, item):
        result = self.collection.insert_one(item)
    def selectAll(self):
        return self.collection.find()
    def selectDistinct(self, key):
        result = self.collection.distinct(key)
        return result

    def inserCompList(self, list):
        result = self.comps.insert_many(list, ordered=False)
# db.jobs.insert_one(doc)

# all_jobs = list(db.jobs.find({}, {'_id':False}))
# print('test')