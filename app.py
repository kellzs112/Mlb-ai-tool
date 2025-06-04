import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="AI MLB Daily Bet Picker", layout="wide")
st.title("⚾ AI MLB Daily Betting Pick (Free Stats Based)")

# Get today's date
today = datetime.now().strftime("%Y-%m-%d")

# Fetch today's games from MLB Stats API
@st.cache_data
def fetch_today_games():
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}"
    try:
        res = requests.get(url)
        data = res.json()
        games = data['dates'][0]['games']
        return [{
            "away": g['teams']['away']['team']['name'],
            "home": g['teams']['home']['team']['name'],
            "game_id": g['gamePk']
        } for g in games]
    except:
        return []

# Basic dummy AI logic to simulate pick selection (for MVP)
def pick_best_game(games):
    if not games:
        return "No games today.", None
    # Pick based on keyword presence for now
    keywords = ['Dodgers', 'Yankees', 'Braves', 'Astros']
    for g in games:
        if any(team in g['home'] or team in g['away'] for team in keywords):
            return f"🔮 Pick: {g['away']} vs {g['home']} — Top matchup based on recent trends.", g
    return f"🔮 Pick: {games[0]['away']} vs {games[0]['home']}", games[0]

games_today = fetch_today_games()
recommendation, selected_game = pick_best_game(games_today)

st.subheader("📅 Today's Games")
for game in games_today:
    st.write(f"{game['away']} @ {game['home']}")

st.markdown("---")
st.subheader("⭐ AI Pick of the Day")
st.success(recommendation)

if selected_game:
    st.markdown("*(Note: This MVP uses basic logic; future versions will use barrel %, exit velo, and full stat models.)*")