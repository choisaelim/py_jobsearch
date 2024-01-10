from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        mongoUrl = "mongodb://localhost:27017"
        self.client = MongoClient(mongoUrl)
        self.db = self.client.local
        self.collection = self.db['jobs']
        print(self.collection)

    def insertList(self, list):
        result = self.collection.insert_many(list)
    def insertOne(self, item):
        result = self.collection.insert_one(item)
    def selectAll(self):
        self.collection.find()
# doc = {
#     'title':'플랫폼베이스 백엔드 개발',
#     'comp':'아프리카TV'
# }

# db.jobs.insert_one(doc)

# all_jobs = list(db.jobs.find({}, {'_id':False}))
# print('test')