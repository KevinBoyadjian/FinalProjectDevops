from datetime import date, timedelta

import requests


SUPPORTED_LEAGUES = {
    "premier-league": {"id": 39, "name": "Premier League"},
    "la-liga": {"id": 140, "name": "La Liga"},
    "serie-a": {"id": 135, "name": "Serie A"},
    "ligue-1": {"id": 61, "name": "Ligue 1"},
}


class FootballAPIService:
    def __init__(self, app_config):
        self.api_key = app_config.get("FOOTBALL_API_KEY", "")
        self.base_url = app_config.get("FOOTBALL_API_BASE_URL", "")
        self.season = app_config.get("SEASON", "2024")

    def _get_headers(self):
        return {
            "x-apisports-key": self.api_key
        }

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"

        response = requests.get(
            url,
            headers=self._get_headers(),
            params=params,
            timeout=20
        )

        # DEBUG TEMPORAIRE
        print("===================================")
        print("URL:", response.url)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text[:500])
        print("===================================")

        response.raise_for_status()
        return response.json()

    def _format_fixture(self, item):
        return {
            "id": item["fixture"]["id"],
            "league": item["league"]["name"],
            "home_team": item["teams"]["home"]["name"],
            "away_team": item["teams"]["away"]["name"],
            "home_score": item["goals"]["home"],
            "away_score": item["goals"]["away"],
            "status": item["fixture"]["status"]["short"],
            "minute": item["fixture"]["status"]["elapsed"] or 0,
            "date": item["fixture"]["date"],
        }

    def _get_league_ids(self, league_key):
        if league_key and league_key in SUPPORTED_LEAGUES:
            return [SUPPORTED_LEAGUES[league_key]["id"]]

        return [league["id"] for league in SUPPORTED_LEAGUES.values()]

    def get_supported_leagues(self):
        return SUPPORTED_LEAGUES

    def get_live_matches(self, league_key=None):
        league_ids = self._get_league_ids(league_key)
        matches = []

        for league_id in league_ids:
            data = self._get(
                "fixtures",
                {
                    "live": "all",
                    "league": league_id
                }
            )

            matches.extend([
                self._format_fixture(item)
                for item in data.get("response", [])
            ])

        return matches

    def get_upcoming_matches(self, league_key=None, limit=10):
        league_ids = self._get_league_ids(league_key)
        matches = []

        today = date.today()

        for league_id in league_ids:
            for day_offset in range(0, 14):
                match_date = today + timedelta(days=day_offset)

                data = self._get(
                    "fixtures",
                    {
                        "league": league_id,
                        "season": self.season,
                        "date": match_date.isoformat()
                    }
                )

                matches.extend([
                    self._format_fixture(item)
                    for item in data.get("response", [])
                ])

                if len(matches) >= limit:
                    return matches[:limit]

        return matches[:limit]

    def get_match_details(self, match_id):
        data = self._get("fixtures", {"id": match_id})
        response = data.get("response", [])

        if not response:
            return None

        item = response[0]

        events_data = self._get(
            "fixtures/events",
            {"fixture": match_id}
        ).get("response", [])

        lineups_data = self._get(
            "fixtures/lineups",
            {"fixture": match_id}
        ).get("response", [])

        home_name = item["teams"]["home"]["name"]
        away_name = item["teams"]["away"]["name"]

        events = []
        for event in events_data:
            events.append({
                "minute": event.get("time", {}).get("elapsed", 0),
                "team": event.get("team", {}).get("name", ""),
                "type": event.get("type", ""),
                "player": event.get("player", {}).get("name", ""),
            })

        home_lineup = []
        away_lineup = []

        for lineup in lineups_data:
            team_name = lineup.get("team", {}).get("name", "")
            players = [
                player["player"].get("name", "")
                for player in lineup.get("startXI", [])
                if player.get("player")
            ]

            if team_name == home_name:
                home_lineup = players
            elif team_name == away_name:
                away_lineup = players

        match = self._format_fixture(item)
        match["events"] = events
        match["lineups"] = {
            "home": home_lineup,
            "away": away_lineup
        }

        return match

    def get_standings(self, league_key="premier-league"):
        league = SUPPORTED_LEAGUES.get(
            league_key,
            SUPPORTED_LEAGUES["premier-league"]
        )

        data = self._get(
            "standings",
            {
                "league": league["id"],
                "season": self.season
            }
        )

        response = data.get("response", [])
        if not response:
            return []

        table = response[0]["league"]["standings"][0]

        return [
            {
                "position": team["rank"],
                "team": team["team"]["name"],
                "points": team["points"],
            }
            for team in table
        ]
