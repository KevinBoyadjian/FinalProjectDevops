from flask import Flask, jsonify, render_template
from config import Config
from services.football_api import FootballAPIService


app = Flask(__name__)
app.config.from_object(Config)

football_service = FootballAPIService(app.config)


@app.route("/")
def index():
    matches = football_service.get_live_matches()
    return render_template("index.html", matches=matches)


@app.route("/standings")
def standings():
    table = football_service.get_standings()
    return render_template("standings.html", standings=table)


@app.route("/match/<int:match_id>")
def match_details(match_id):
    match = football_service.get_match_details(match_id)
    return render_template("match.html", match=match)


@app.route("/api/live")
def api_live():
    matches = football_service.get_live_matches()
    return jsonify(matches)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
