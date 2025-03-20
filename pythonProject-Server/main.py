from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS
from player import Player
from functools import wraps
import random

app = Flask(__name__)

CORS(app, supports_credentials=True)
players = []


# decorator is conected:
def isConnected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = request.cookies.get('user')
        if name:
            x = func(*args, **kwargs)
            return x
        else:
            return abort(401)

    return wrapper


# פונקציה להגרלת מילה
@app.route('/lottery/<num>', methods=['GET'])
@isConnected
def lottery(num):
    try:
        num = int(num)
    except:
        return abort(400)
    with open("../pythonProject-Server/words.txt", 'r') as file:
        content = file.read()
        listWord = content.split(" ")
        random.shuffle(listWord)  # ערבוב הרשימה
        if num < len(listWord):
            return listWord[num]
        else:
            return listWord[num % len(listWord)]


# signin
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()  # חילוץ הנתונים מהבקשה
    name = data.get('name')
    password = data.get('password')
    Id = data.get('Id')
    exsistPlayer = next((p for p in players if p.password == password), None)
    if (exsistPlayer != None):
        return abort(409)
    newPlayer = Player(name, Id, password)
    players.append(newPlayer)
    response = make_response("Welcome")
    response.set_cookie("user", name, max_age=600, httponly=True, secure=False, samesite='None')
    writeToFile()  #עדכון הקובץ בנתונים החדשים
    readFile()   #קריאת הקובץ ועדכון מערך המשחקים
    return response


# login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # חילוץ הנתונים מהבקשה
    name = data.get('name')
    password = data.get('password')
    currentPlayer = next((p for p in players if p.password == password), None)
    if (currentPlayer == None):
        return abort(404)
    else:
        response = make_response("Welcome")
        response.set_cookie("user", currentPlayer.name, max_age=600, httponly=True, secure=False, samesite='None')
        return response


# פונקציה לסיום המשחק
@app.route('/finish', methods=['POST'])
@isConnected
def finish():
    data = request.get_json()  # חילוץ הנתונים מהבקשה
    win = data.get('win')
    word = data.get('word')
    name = request.cookies.get('user')
    currentPlayer = next((p for p in players if p.name == name), None)
    if currentPlayer == None:
        return abort(401)
    currentPlayer.gamesNum = currentPlayer.gamesNum + 1
    currentPlayer.words.add(word)
    if win:
        currentPlayer.win = currentPlayer.win + 1
    response = make_response("OK")
    return response


#  פונקציה- log out-מחיקת עוגיה ורישום לקובץ של הנתונים
@app.route('/del-cookie', methods=['GET'])
@isConnected
def delCookie():
    writeToFile()
    readFile()
    response = make_response("Welcome")
    # נתתי ערך פג תוקף לעוגיה, ולכן היא כבר לא קיימת
    response.set_cookie("user", "", max_age=0, httponly=True, secure=False, samesite='None')
    return response


# פונקצית היסטוריה
@app.route('/history', methods=['GET'])
@isConnected
def history():
    name = request.cookies.get('user')
    currentPlayer = next((p for p in players if p.name == name), None)
    if currentPlayer == None:
        return abort(404)
    my_history = {
        "gamesNum": currentPlayer.gamesNum,
        "words": list(currentPlayer.words),
        "win": currentPlayer.win
    }
    return jsonify(my_history)


def readFile():
    players.clear()  # במידה וקוראים את הקובץ במהלך התוכנית, יש לרוקן את המערך לפני שממלאים אותו שוב
    with open("./players.txt", 'r') as file:
        content = file.readlines()
        for line in content:
            data = {}
            for item in line.split(","):
                key, value = item.split(":")
                data[key] = value.strip()
            newPlayer = Player(data['name'], (data['Id']), data['password'])
            newPlayer.gamesNum = int(data['gamesNum'])
            newPlayer.win = int(data['win'])
            newPlayer.words = set(data['words'].strip("{}").split())
            players.append(newPlayer)


def writeToFile():
    listPlayers = [str(item) + "\n" for item in players]
    with open("./players.txt", 'w') as file:
        file.writelines(listPlayers)


if __name__ == "__main__":
    readFile()  # בתחילת המשחק הקובץ נקרא
    app.run(debug=True)
