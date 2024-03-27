from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
import certifi

#init
app = Flask(__name__)

uri = "mongodb+srv://root:root@cluster0.qyyrcuj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#sets up certificat
ca = certifi.where()
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)

db = client.Steam
games = db['Game Names']
categories = db.Categories


#routes
@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("layout.html", title="layout page", games = games)


#@app.route("/show_games/<id>", methods = ["POST", "GET"])
#def show_games(id):
 #   if request.method == "POST":
  #      form = TodoForm(request.form)
#
 #       db.todo_flask.find_one_amd_update({"_id"})

# setup mongoDB
app.config["MONGO_URI"] = "mongodb+srv://root:root@cluster0.qyyrcuj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongodb_client = PyMongo(app)
db = mongodb_client.db

#run
if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)
