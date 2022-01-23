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
    print(name, school)
    result = mongo_driver.search(name=name, school=school)
    return result
    
name = "Chinh"
school = School.ANY


app.run(debug=True)