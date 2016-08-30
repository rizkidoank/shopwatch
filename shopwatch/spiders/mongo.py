from pymongo import MongoClient
conn = MongoClient(host="localhost")
db = conn.shopwatch

data = db.products


for i in data.find({},{"desc":1}):
    print(i)