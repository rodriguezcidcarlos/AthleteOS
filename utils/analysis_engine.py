import pandas as pd

from utils.decision_engine import analyze_player
from utils.analytics import calculate_load_trend


def analyze_player_full(player_df: pd.DataFrame):

    last = player_df.iloc[-1]

    decision = analyze_player(player_df)

    trend = calculate_load_trend(player_df)

    return {

        "player_id": last["player_id"],

        "player": last["player"],

        "daily_load": int(last["daily_load"]),

        "acwr": round(float(last["acwr"]), 2),

        "status": decision["status"],

        "priority": None,

        "alerts": decision["alerts"],

        "recommendation": decision["recommendation"],

        "trend": trend["trend"],

        "change": trend["change"]

    }

from utils.analysis_engine import analyze_player_full

print("\nPLAYER ANALYSIS")

player_df = df[df["player"] == "Carlos"]

analysis = analyze_player_full(player_df)

print(analysis)