import pymongo 
from pprint import pprint

client = pymongo.MongoClient("mongodb+srv://penn-mail-search:penn-mail-search@us-east.36o9t.mongodb.net/penn-mail-search?retryWrites=true&w=majority")
db = client['penn-mail-search']
collection = db['student']

rec={
    'title':'MongoDB and Python', 
    'description': 'MongoDB is no SQL database', 
    'tags': ['mongodb', 'database', 'NoSQL'], 
    'viewers': 104 
}

collection.insert_one({"foo": "bar"})

