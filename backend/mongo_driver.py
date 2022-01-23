import pymongo 
from enumerations import School
from pprint import pprint
from bson.json_util import dumps, loads

client = pymongo.MongoClient("mongodb+srv://penn-mail-search:penn-mail-search@us-east.36o9t.mongodb.net/penn-mail-search?retryWrites=true&w=majority")
db = client['penn-mail-search']
collection = db['student']


class MongoDriver:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://penn-mail-search:penn-mail-search@us-east.36o9t.mongodb.net/penn-mail-search?retryWrites=true&w=majority")
        self.db = client['penn-mail-search']
        self.collectoin = db['student']

    def search(self, name = '', school : School = School.ANY):
        suggestions_cursor = collection.find(
            filter={'Name': {'$regex': name, '$options': 'i'},
                    'School': {'$in': school.value}
                    }, 
            limit=8)
        
        json_data = dumps(list(suggestions_cursor))
        return json_data

driver = MongoDriver()
