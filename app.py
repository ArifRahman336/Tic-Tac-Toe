from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from game import GameState
from ai import find_best_move

app = Flask(__name__)
app.secret_key = "ultimate-ttt-secret"

state = None

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- SETTINGS ----------------
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        session["mode"] = request.form.get("mode", "ai")
        session["player1_name"] = request.form.get("player1_name", "Player 1")
        session["player1_symbol"] = request.form.get("player1_symbol", "X")

        if session["mode"] == "pvp":
            session["player2_name"] = request.form.get("player2_name", "Player 2")
        else:
            session.pop("player2_name", None)

        session["difficulty"] = request.form.get("difficulty", "medium")
        return redirect(url_for("home"))

    return render_template(
        "settings.html",
        mode=session.get("mode", "ai"),
        player1_name=session.get("player1_name", ""),
        player2_name=session.get("player2_name", ""),
        player_color=session.get("player1_symbol", "X"),
        difficulty=session.get("difficulty", "medium")
    )

# ---------------- START GAME ----------------
@app.route("/start/<mode>")
def start(mode):
    global state

    state = GameState()
    session["mode"] = mode
    session.pop("winner", None)

    p1_symbol = session.get("player1_symbol", "X")
    p2_symbol = "O" if p1_symbol == "X" else "X"

    session["p1_symbol"] = p1_symbol
    session["p2_symbol"] = p2_symbol

    # ✅ FIX: Player 1 always starts
    state.current_player = p1_symbol

    if mode == "ai":
        state.human = p1_symbol
        state.ai = p2_symbol
        state.difficulty = session.get("difficulty", "medium")
    else:
        state.human = p1_symbol
        state.ai = None

    return redirect(url_for("game"))


# ---------------- GAME ----------------
@app.route("/game")
def game():
    return render_template("game.html")

# ---------------- MOVE ----------------
@app.route("/move", methods=["POST"])
def move():
    global state
    if state is None:
        return jsonify({"error": "Game not initialized"})

    data = request.get_json()
    b, c = int(data["board"]), int(data["cell"])

    if not state.make_move(b, c, state.current_player):
        return jsonify({"error": "Invalid move"})

    winner = state.check_global_win()
    ai_move = None

    if not winner and session.get("mode") == "ai":
        depth = {"easy":1, "medium":3, "hard":5}.get(session.get("difficulty"), 3)
        ai_move = find_best_move(state, depth)
        if ai_move:
            state.make_move(ai_move[0], ai_move[1], state.current_player)
            winner = state.check_global_win()

    return jsonify({
        "board": state.board,
        "smallBoardStatus": state.smallBoardStatus,
        "nextBoard": state.nextBoard,
        "aiMove": ai_move,
        "winner": winner,
        "currentPlayer": state.current_player
    })

# ---------------- RESET ----------------
@app.route("/reset", methods=["POST"])
def reset():
    global state

    state = GameState()
    state.current_player = session.get("p1_symbol", "X")


    mode = session.get("mode", "ai")

    p1_symbol = session.get("p1_symbol", "X")
    p2_symbol = session.get("p2_symbol", "O")

    # 🔑 ALWAYS RESET CURRENT PLAYER
    state.current_player = p1_symbol

    if mode == "ai":
        state.human = p1_symbol
        state.ai = p2_symbol
        state.difficulty = session.get("difficulty", "medium")
    else:
        # PvP
        state.human = p1_symbol
        state.ai = None

    session.pop("winner", None)

    return jsonify({
        "board": state.board,
        "smallBoardStatus": state.smallBoardStatus,
        "nextBoard": state.nextBoard,
        "currentPlayer": state.current_player
    })



if __name__ == "__main__":
    app.run(debug=True)
