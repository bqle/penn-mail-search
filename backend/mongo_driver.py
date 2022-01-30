import pymongo 
from enumerations import School
from pprint import pprint
from bson.json_util import dumps, loads
import json
import os

if not os.path.exists('.config'):
    print("config file does not exist")
    quit()

with open('.config', 'r') as f:
    config = json.loads(f.read())

mondodb_username = config['mongodb-username']
mongodb_password = config['mongodb-password']
mongodb_url = config['mongodb-url']

class MongoDriver:
    def __init__(self):
        try: 
            self.client = pymongo.MongoClient(
                "mongodb+srv://{}:{}@{}/penn-mail-search?retryWrites=true&w=majority".format(mondodb_username, mongodb_password, mongodb_url))
        except:
            print("Login Error: incorrect username, password, or url for database\n")
            raise

        self.db = self.client['penn-mail-search']
        self.collection = self.db['student']

    def search(self, name = '', school : School = School.ANY):
        suggestions_cursor = self.collection.find(
            filter={'$or': [{'Name': {'$regex': name, '$options': 'i'}},
                    {'Email': {'$regex': name, '$options': 'i'}}],
                    'School': {'$in': school.value}
                    }, 
            limit=8)
        json_data = dumps(list(suggestions_cursor))
        return json_data

