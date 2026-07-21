from config import DATA_FILE

from utils.io import load_training_data
from core.load import (
    calculate_daily_load,
    calculate_acwr
)

from utils.decision_engine import analyze_squad
from utils.priority_engine import generate_intervention_list
from utils.analytics import calculate_load_trend


print("=" * 60)
print("ATHLETEOS TEST ENGINE")
print("=" * 60)

df = load_training_data(DATA_FILE)

df = calculate_daily_load(df)

df = calculate_acwr(df)

print("\nDatos cargados:", len(df))

print("\n")

# -----------------------------
# Squad
# -----------------------------

squad = analyze_squad(df)

print("SQUAD")
print(squad.to_string())

print("\n")

# -----------------------------
# Action Center
# -----------------------------

actions = generate_intervention_list(squad)

print("ACTION CENTER")
print(actions.to_string())

print("\n")

# -----------------------------
# Tendencias
# -----------------------------

print("LOAD TRENDS")

for player_id, player_df in df.groupby("player_id"):

    trend = calculate_load_trend(player_df)

    print(
        player_df.iloc[-1]["player"],
        trend
    )