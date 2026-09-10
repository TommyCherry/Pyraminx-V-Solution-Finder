from flask import Flask, render_template, request
from Solver2026 import Pyraminx, bfs, MOVES

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    solutions = None
    error = None
    scramble = ""
    p = Pyraminx()

    if request.method == "POST":
        scramble = request.form["scramble"]
        max_depth = int(request.form["max_depth"])

        moves = scramble.split()

        if any(move not in MOVES for move in moves):
            error = "Invalid scramble. Use only U, U', L, L', R, R', B, and B'."
        elif max_depth < 1 or max_depth > 7:
            error = "Maximum solution length must be between 1 and 7."
        else:
            p.scramble(scramble)
            solutions = bfs(p, max_depth)

    face_colors = p.get_face_colors()

    return render_template(
        "index.html",
        solutions=solutions,
        face_colors=face_colors,
        error=error,
        scramble=scramble
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)