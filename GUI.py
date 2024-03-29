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
categories = db['Categories']
players = db['Playtime']
genres = db['Genres']
tags = db['Tags']
publishers = db['Publishers']
developers = db['Developers']
platforms = db['Platforms']
studios = db['Studios']

gameCategoryRelationships = db['Game-Category Relationships']
gameGenreRelationships = db['Game-Genre Relationships']
gameTagRelationships = db['Game-Tag Relationships']
gameStudioRelationships = db['Game-Studio Relationships']



skipVal=0
curPage=0


pageSize = 10
numOfPages = 0


## ROUTES ##
#determines which html file to load, and passes the variables to the html page
@app.route("/", methods=["POST", "GET"])
def index():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 0:
        curPage=0
        skipVal=0

    if request.method == 'POST':
        next = request.form.get("next")
        prev = request.form.get("last")
        if next is not None:
            if skipVal + 1 < numOfPages:
                skipVal += 1
        if prev is not None:
            if skipVal > 0:
                skipVal -= 1
        return redirect(url_for('index'))

    g = games.find().skip(skipVal*pageSize).limit(pageSize)
    numOfPages = games.count_documents({})//pageSize

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_games.html", title="View Games", games=g, pgCount=numOfPages, currentPage=skipVal+1, first=f)


@app.route("/view_players", methods=["POST", "GET"])
def view_players():
    global skipVal
    global numOfPages
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

    page_size = 10
    page_number = 0  # First page
    pipeline = [
        {"$group": {"_id": "$playerID"}},
        {"$skip": skipVal*10},
        {"$limit": 10},
        {"$sort": {"_id": 1}}
    ]



    pl = players.aggregate(pipeline)
    
    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_players.html", title="View Players", players=pl, pgCount=numOfPages, currentPage=skipVal+1, first=f)


@app.route("/search", methods=["POST", "GET"])
def search():
    r = []
    if request.method == "POST":
        req = request.form.get("term")
        op = request.form['options']
        # code to search our ARM for matching key
        #examples: if you play the search term, what other tags/categories/genres/games might you like
        #recommendation system? or somthing like that
        r = [{"text": "string"}]

        return render_template("search.html", title="Search", res=r)
    return render_template("search.html", title="Search")


@app.route("/graph")
def graph():
    return render_template("graphs.html", title="Graphs")

## RUN ##
#runs the app
if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)


