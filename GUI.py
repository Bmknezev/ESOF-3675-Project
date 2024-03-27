from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#init
app = Flask(__name__)

#routes
@app.route("/")
def index():
    return render_template("layout.html", title="layout page")
#@app.route("/show_games/<id>", method = ["POST", "GET"])
#def show_games(id):
   # if request.method == "POST":
        #form = TodoForm(request.form)

       # db.todo_flask.find_one_amd_update({"_id"})

# setup mongoDB
app.config["MONGO_URI"] = "mongodb+srv://root:root@cluster0.qyyrcuj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongodb_client = PyMongo(app)
db = mongodb_client.db

#run
if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)
