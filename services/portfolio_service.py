import json
from pathlib import Path


def load_portfolio():
    file_path = Path("portfolio.json")

    if not file_path.exists():
        raise FileNotFoundError("找不到 portfolio.json")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_stocks():
    portfolio = load_portfolio()

    holdings = portfolio.get("holdings", [])
    watchlist = portfolio.get("watchlist", [])

    return holdings + watchlist
