from flask import Flask, request, jsonify
from mongo_driver import MongoDriver
from enumerations import School
import json

app = Flask(__name__)
mongo_driver = MongoDriver()
school_options = [School.ANY, School.COLLEGE_OF_ARTS_AND_SCIENCES, School.ENGINEERING, School.NURSING, School.WHARTON]

@app.route("/search")
def search():
    # run a search and return top 8 results
    name = request.args.get('name')
    name = name if name is not None else ''

    school = request.args.get('school')
    school = school_options[int(school)] if school is not None else School.ANY
    result = mongo_driver.search(name=name, school=school)
    return result
    
@app.route("/")
def home():
    return "Hello world"

if __name__ == '__main__':
    app.run(port=5000)