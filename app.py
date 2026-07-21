from pathlib import Path
from dash import Dash, html

from utils.io import load_training_data
from core.engine import AthleteOSCore

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"

df = load_training_data(DATA_FILE)

core = AthleteOSCore()
df_core = core.prepare_data(df)

app = Dash(__name__)

server = app.server

print("SERVER EXPORT:", server, flush=True)

print("SERVER CREATED OK", flush=True)

app.layout = html.Div([
    html.H1("AthleteOS"),
    html.P(f"Registros: {len(df_core)}")
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)