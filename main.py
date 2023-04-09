# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

app = Flask(__name__)
CORS(app)

data = json.load(open('db.json'))

@app.get("/players")
def get_players():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=data["user"],
            password=data["password"],
            port=data["port"],
            database=data["database"],
        )

        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT DISTINCT Player, NbaPlayerId FROM player")
        player_names = mycursor.fetchall()
        mydb.close()
        mycursor.close()
        return jsonify(player_names)
    except NameError:
        return NameError, 400

@app.get("/player")
def get_player():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=data["user"],
            password=data["password"],
            port=data["port"],
            database=data["database"],
        )

        mycursor = mydb.cursor(dictionary=True)
        nba_player_id = request.args.get('id')
        mycursor.execute(f"SELECT SeasonYear as id, player, team, gp, min, pts, reb, ast, tov, stl, blk, ROUND(rdef, 2) as rdef, ROUND(pdef, 2) as pdef, ROUND(def, 2) as def, team, position FROM player WHERE NbaPlayerId = %s ORDER BY id", (nba_player_id,))
        player = mycursor.fetchall()
        mydb.close()
        mycursor.close()
        return jsonify(player)
    except NameError:
        return NameError, 400

@app.get("/top/players")
def get_top_players():
    current_year = "22/23"
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=data["user"],
            password=data["password"],
            port=data["port"],
            database=data["database"],
        )

        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(f"SELECT id, player, team, position, gp, min, pts, reb, ast, tov, stl, blk, ROUND(rdef, 2) as rdef, ROUND(pdef, 2) as pdef, ROUND(def, 2) as def FROM player WHERE SeasonYear = %s ORDER BY DEF DESC LIMIT 20", (current_year,))
        player = mycursor.fetchall()
        mydb.close()
        mycursor.close()
        return jsonify(player)
    except NameError:
        return NameError, 400

@app.get("/season")
def get_season():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=data["user"],
            password=data["password"],
            port=data["port"],
            database=data["database"],
        )
        mycursor = mydb.cursor(dictionary=True)

        year = request.args.get('year')

        mycursor.execute(f"SELECT id, player, team, position, gp, min, pts, reb, ast, tov, stl, blk, ROUND(rdef, 2) as rdef, ROUND(pdef, 2) as pdef, ROUND(def, 2) as def FROM player WHERE SeasonYear = %s ORDER BY DEF DESC", (year,))
        player = mycursor.fetchall()
        mydb.close()
        mycursor.close()
        return jsonify(player)
    except NameError:
        return NameError, 400

@app.get("/status")
def get_player_status():
    try:
        player_id = request.args.get('id')
        player = [player for player in players.get_players() if player['id'] == int(player_id)][0]
        print(player)
        return jsonify(active=player['is_active'])
    except NameError:
        return NameError, 400

@app.get("/top/player")
def get_top_player():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=data["user"],
            password=data["password"],
            port=data["port"],
            database=data["database"],
        )
        current_year = request.args.get('year').replace("-", "/")
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(f"SELECT player, ROUND(rdef, 2) as rdef, ROUND(pdef, 2) as pdef, ROUND(def, 2) as def FROM player WHERE SeasonYear = %s ORDER BY DEF DESC LIMIT 1", (current_year,))
        player_obj = mycursor.fetchall()[0]
        mydb.close()
        mycursor.close()
        player_name = player_obj["player"]
        player = [player for player in players.get_players() if player['full_name'] == player_name][0]
        player_obj["image"] = "https://cdn.nba.com/headshots/nba/latest/1040x760/" + str(player['id']) + ".png?imwidth=1040&imheight=760"
        return jsonify(player_obj)
    except NameError:
        return NameError, 400