# app.py
from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

data = json.load(open('db.json'))
mydb = mysql.connector.connect(
    host="localhost",
    user=data["user"],
    password=data["password"],
    port=data["port"],
    database=data["database"]
)

mycursor = mydb.cursor()

@app.get("/players")
def get_players():
    mycursor.execute("SELECT DISTINCT Player FROM player")
    playerNames = mycursor.fetchall()
    return jsonify(playerNames)

@app.get("/player")
def get_player():
    try:
        player_name = request.args.get('name')
        print("lala")
        print(player_name)
        mycursor.execute(f"SELECT * FROM player WHERE Player = %s", (player_name,))
        playerNames = mycursor.fetchall()
    except NameError:
        return NameError, 400
    return jsonify(playerNames)
