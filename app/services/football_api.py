import requests


class FootballAPIService:
    def __init__(self, app_config):
        self.api_key = app_config.get("FOOTBALL_API_KEY", "")
        self.base_url = app_config.get("FOOTBALL_API_BASE_URL", "")
        self.league_id = app_config.get("LEAGUE_ID", "")
        self.season = app_config.get("SEASON", "")

    def _get_headers(self):
        return {
            "x-apisports-key": self.api_key
        }

    def get_live_matches(self):
        return [
            {
                "id": 1,
                "home_team": "Maccabi Haifa",
                "away_team": "Hapoel Be'er Sheva",
                "home_score": 2,
                "away_score": 1,
                "status": "Live",
                "minute": 67
            },
            {
                "id": 2,
                "home_team": "Maccabi Tel Aviv",
                "away_team": "Beitar Jerusalem",
                "home_score": 0,
                "away_score": 0,
                "status": "HT",
                "minute": 45
            }
        ]

    def get_match_details(self, match_id):
        return {
            "id": match_id,
            "home_team": "Maccabi Haifa",
            "away_team": "Hapoel Be'er Sheva",
            "home_score": 2,
            "away_score": 1,
            "status": "Live",
            "minute": 67,
            "events": [
                {"minute": 12, "team": "Maccabi Haifa", "type": "Goal", "player": "Player A"},
                {"minute": 29, "team": "Hapoel Be'er Sheva", "type": "Yellow Card", "player": "Player B"},
                {"minute": 52, "team": "Maccabi Haifa", "type": "Goal", "player": "Player C"},
            ],
            "lineups": {
                "home": ["Player A", "Player C", "Player D", "Player E"],
                "away": ["Player B", "Player F", "Player G", "Player H"]
            }
        }

    def get_standings(self):
        return [
            {"position": 1, "team": "Maccabi Tel Aviv", "points": 58},
            {"position": 2, "team": "Maccabi Haifa", "points": 55},
            {"position": 3, "team": "Hapoel Be'er Sheva", "points": 50},
            {"position": 4, "team": "Beitar Jerusalem", "points": 42},
        ]
