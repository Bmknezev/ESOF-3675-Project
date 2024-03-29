import math

from flask import Flask, render_template, request, redirect, url_for, json
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
import certifi
import re

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
players = db['Playtime']
categories = db['Categories']
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

#arm database connections

gameCategoryARM = db['games-categories ARM']
gameGenreARM = db['game-genres ARM']
gameTagARM = db['games-tags ARM']
playerGenreARM = db['players-genres ARM']
playerTagARM = db['players-tags ARM']

#defines variable used in the GUI
skipVal=0
curPage=0

pageSize = 10
numOfPages = 0


## ROUTES ##
#determines which html file to load, and passes the variables to the html page

#games table page
@app.route("/games", methods=["POST", "GET"])
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
    numOfPages = math.ceil(games.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_games.html", title="View Games", games=g, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#players table page
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
        {"$sort": {"playerID": 1}}
    ]



    pl = players.aggregate(pipeline)
    
    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_players.html", title="View Players", players=pl, pgCount=numOfPages, currentPage=skipVal+1, first=f)


#categories table page
@app.route("/view_categories", methods=["POST", "GET"])
def view_categories():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 2:
        curPage=2
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
        return redirect(url_for('view_categories'))

    c = categories.find().sort({"_id": 1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(categories.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_categories.html", title="View Categories", categories=c, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#Genres table page
@app.route("/view_genres", methods=["POST", "GET"])
def view_genres():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 3:
        curPage=3
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
        return redirect(url_for('view_genres'))

    g = genres.find().sort({"_id": 1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(genres.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_genres.html", title="View Genre", genres=g, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#Tags table page
@app.route("/view_tags", methods=["POST", "GET"])
def view_tags():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 4:
        curPage=4
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
        return redirect(url_for('view_tags'))

    t = tags.find().sort({"_id": 1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(tags.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_tags.html", title="View Tags", tags=t, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#Tags table page
@app.route("/view_publishers", methods=["POST", "GET"])
def view_publishers():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 5:
        curPage=5
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
        return redirect(url_for('view_publishers'))

    p = publishers.find().sort({"_id": 1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(publishers.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_publishers.html", title="View Publishers", publishers=p, pgCount=numOfPages, currentPage=skipVal+1, first=f)


#Developers table page
@app.route("/view_developers", methods=["POST", "GET"])
def view_developers():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 6:
        curPage=6
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
        return redirect(url_for('view_developers'))

    d = developers.find().sort({"_id": 1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(developers.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_developers.html", title="View Developers", devs=d, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#Platforms table page
@app.route("/view_platforms", methods=["POST", "GET"])
def view_platforms():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 6:
        curPage=6
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
        return redirect(url_for('view_platforms'))

    p = platforms.find().sort({"_id": 1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(platforms.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_platforms.html", title="View Platforms", plats=p, pgCount=numOfPages, currentPage=skipVal+1, first=f)



#search page
@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        req = request.form.get("term")
        op = request.form['options']
        query = {"antecedents": req.title()}
        if op == "genre":
            r = playerGenreARM.find(query).sort({"confidence": -1})
        elif op == "tag":
            r = playerTagARM.find(query).sort({"confidence": -1})
        
        
        
        return render_template("search.html", title="Search", res=r)
    return render_template("search.html", title="Search")


#graphs page
@app.route("/graph")
def graph():
    return render_template("graphs.html", title="Graphs")

#homepage
@app.route("/")
def homepage():
    return render_template("homepage.html", title="games unlimited games")



## RUN ##
#runs the app
if __name__ == '__main__':
    app.secret_key = 'secretivekey'
    app.run(debug=True)


