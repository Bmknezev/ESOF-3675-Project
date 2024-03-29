from flask import Flask, render_template, request, redirect, url_for, json
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
players = db.Playtime

#global skipVal
skipVal=0
curPage=0



## ROUTES ##
#determines which html file to load, and passes the variables to the html page
@app.route("/", methods=["POST", "GET"])
def index():
    global skipVal
    global curPage
    if curPage != 0:
        curPage=0
        skipVal=0

    if request.method == 'POST':
        next = request.form.get("next")
        prev = request.form.get("last")
        if next is not None:
            skipVal += 1
        if prev is not None:
            if skipVal > 0:
                skipVal -= 1
        return redirect(url_for('index'))
    g = games.find().skip(skipVal*20).limit(20)
    return render_template("view_games.html", title="View Games", games=g)


@app.route("/view_players", methods=["POST", "GET"])
def view_players():
    global skipVal
    global curPage
    if curPage != 1:
        curPage=1
        skipVal=0
    if request.method == "POST":
        next = request.form.get("next")
        prev = request.form.get("last")
        if next is not None:
            skipVal += 1
        if prev is not None:
            if skipVal > 0:
                skipVal -= 1
        return redirect(url_for('view_players'))

    page_size = 20
    page_number = 0  # First page
    pipeline = [
        {"$group": {"_id": "$playerID"}},
        {"$skip": skipVal*20},
        {"$limit": 20},
  {"$sort": {"_id": 1}}
    ]

    #p = players.distinct("playerID")
    
    pl = players.aggregate(pipeline)

    p = players.distinct("playerID")
    
    
    return render_template("view_players.html", title="View Players", players=pl)





## RUN ##
#runs the app
if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)
