import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "")
    FOOTBALL_API_BASE_URL = os.getenv("FOOTBALL_API_BASE_URL", "https://v3.football.api-sports.io")
    LEAGUE_ID = os.getenv("LEAGUE_ID", "328")  # à ajuster selon l'API choisie
    SEASON = os.getenv("SEASON", "2025")
