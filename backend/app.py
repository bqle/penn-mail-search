from flask import Flask, request

app = Flask(__name__)

@app.route("/search")
def search():
    key = request.args.get('key')
    # run a search and return top 10 results
    
    return "Hello, World!"

app.run()