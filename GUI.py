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
gameGenreARM = db['games-genres ARM']
gameTagARM = db['games-tags ARM']
playerGenreARM = db['players-genres ARM']
playerTagARM = db['players-tags ARM']
gamesGamesARM = db['games-games ARM']

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

#pulbishers table page
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
    if curPage != 7:
        curPage=7
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
        elif op == "game":
            r = gamesGamesARM.find(query).sort({"confidence": -1})

        
        
        return render_template("search.html", title="Search", res=r, searchOp=op)
    return render_template("search.html", title="Search")


#games categories datamining page
@app.route("/view_gameCategoryARM", methods=["POST", "GET"])
def view_gameCategoryARM():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 8:
        curPage=8
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
        return redirect(url_for('view_gameCategoryARM'))

    r = gameCategoryARM.find().sort({"confidence": -1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(gameCategoryARM.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_gameCategoryARM.html", title="ARM", results=r, pgCount=numOfPages, currentPage=skipVal+1, first=f)


#games genres datamining page
@app.route("/view_gameGenreARM", methods=["POST", "GET"])
def view_gameGenreARM():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 9:
        curPage=9
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
        return redirect(url_for('view_gameGenreARM'))

    r = gameGenreARM.find().sort({"confidence": -1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(gameGenreARM.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_gamesGenreARM.html", title="ARM", results=r, pgCount=numOfPages, currentPage=skipVal+1, first=f)


#games tags datamining page
@app.route("/view_gameTagARM", methods=["POST", "GET"])
def view_gameTagARM():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 10:
        curPage=10
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
        return redirect(url_for('view_gameTagARM'))

    r = gameTagARM.find().sort({"confidence": -1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(gameTagARM.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_gameTagARM.html", title="ARM", results=r, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#games genres datamining page
@app.route("/view_playerGenreARM", methods=["POST", "GET"])
def view_playerGenreARM():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 11:
        curPage=11
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
        return redirect(url_for('view_playerGenreARM'))

    r = playerGenreARM.find().sort({"confidence": -1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(playerGenreARM.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_playerGenreARM.html", title="ARM", results=r, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#games genres datamining page
@app.route("/view_playerTagARM", methods=["POST", "GET"])
def view_playerTagARM():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 12:
        curPage=12
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
        return redirect(url_for('view_playerTagARM'))

    r = playerTagARM.find().sort({"confidence": -1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(playerTagARM.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_playerTagARM.html", title="ARM", results=r, pgCount=numOfPages, currentPage=skipVal+1, first=f)

#games games datamining page
@app.route("/view_gameGameARM", methods=["POST", "GET"])
def view_gameGameARM():
    global skipVal
    global numOfPages
    global curPage
    if curPage != 12:
        curPage=12
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
        return redirect(url_for('view_gameGameARM'))

    r = gamesGamesARM.find().sort({"confidence": -1}).skip(skipVal*pageSize).limit(pageSize)
    numOfPages = math.ceil(gamesGamesARM.count_documents({})/pageSize)

    if skipVal > 0:
        f = False
    else:
        f = True
    return render_template("view_gameGameARM.html", title="ARM", results=r, pgCount=numOfPages, currentPage=skipVal+1, first=f)



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


