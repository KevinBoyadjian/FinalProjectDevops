from flask import Flask, jsonify, render_template, request

from config import Config
from services.football_api import FootballAPIService


app = Flask(__name__)
app.config.from_object(Config)

football_service = FootballAPIService(app.config)


@app.route("/")
def index():
    league = request.args.get("league")

    matches = football_service.get_live_matches(league)
    mode = "live"

    if not matches:
        matches = football_service.get_upcoming_matches(league)
        mode = "upcoming"

    return render_template(
        "index.html",
        matches=matches,
        mode=mode,
        selected_league=league or "all",
        leagues=football_service.get_supported_leagues(),
    )


@app.route("/standings")
def standings():
    league = request.args.get("league", "premier-league")
    table = football_service.get_standings(league)

    return render_template(
        "standings.html",
        standings=table,
        selected_league=league,
        leagues=football_service.get_supported_leagues(),
    )


@app.route("/match/<int:match_id>")
def match_details(match_id):
    match = football_service.get_match_details(match_id)

    if match is None:
        return "Match not found", 404

    return render_template("match.html", match=match)


@app.route("/api/live")
def api_live():
    league = request.args.get("league")

    matches = football_service.get_live_matches(league)
    mode = "live"

    if not matches:
        matches = football_service.get_upcoming_matches(league)
        mode = "upcoming"

    return jsonify({
        "mode": mode,
        "matches": matches
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
