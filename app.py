print("000 APP START", flush=True)

from pathlib import Path
from dash import Dash, html

from utils.io import load_training_data

print("IO IMPORT OK", flush=True)


BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


print("ANTES LOAD TRAINING", flush=True)

df = load_training_data(DATA_FILE)

print("LOAD TRAINING OK", flush=True)
print(df.shape, flush=True)
print(df.columns.tolist(), flush=True)


print(df.head().to_string(), flush=True)

print("ANTES CORE", flush=True)

from core.engine import AthleteOSCore

print("CORE IMPORT OK", flush=True)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("AthleteOS"),
        html.P(f"Registros: {len(df)}")
    ]
)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )