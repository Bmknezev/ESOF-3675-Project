from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
import certifi

#init app
app = Flask(__name__)


## SETS UP MONGODB CONNECTION ##

uri = "mongodb+srv://root:root@cluster0.qyyrcuj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#sets up certificat
ca = certifi.where()
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)

#test connection, not needed but good for bug testing
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#defines the database variables
db = client.Steam
games = db['Games Names']
categories = db.Categories





## ROUTES ##
#determines which html file to load, and passes the variables to the html page
@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))
    g = games.find().limit(20)
    return render_template("view_games.html", title="View Games", games=g)


## RUN ##
#runs the app
if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)
