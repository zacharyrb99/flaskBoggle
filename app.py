from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def home_page():
    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    return render_template("index.html", board=board, highscore=highscore, plays=plays)

@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, word)

    return jsonify({'result': result})

@app.route("/final-score", methods=["POST"])
def final_score():
    final_score = request.json["score"]
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    session["plays"] = plays + 1
    session["highscore"] = max(final_score, highscore)

    return jsonify(brokeHighScore = final_score > highscore)