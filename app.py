from pathlib import Path
from dash import Dash, html

from utils.io import load_training_data
from core.engine import AthleteOSCore


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


# ==========================
# LOAD DATA
# ==========================

df = load_training_data(DATA_FILE)

core = AthleteOSCore()

df_core = core.prepare_data(df)


print("ANTES ANALYZE SQUAD", flush=True)

squad = core.analyze_squad(df_core)

print("SQUAD OK", flush=True)

print(
    squad[
        [
            "player",
            "acwr",
            "status"
        ]
    ].head().to_string(),
    flush=True
)


print("ANTES PRIORITY", flush=True)

priority = core.prioritize_squad(squad)

print("PRIORITY OK", flush=True)

print(
    priority.head().to_string(),
    flush=True
)

# ==========================
# DASH APP
# ==========================

app = Dash(__name__)

server = app.server

print("SERVER EXPORT:", server, flush=True)


app.layout = html.Div([

    html.H1("AthleteOS"),

    html.P(
        f"Registros: {len(df_core)}"
    ),

    html.P(
        f"Jugadores analizados: {len(squad)}"
    )

])


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )