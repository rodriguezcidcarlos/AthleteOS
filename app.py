from pathlib import Path
from dash import Dash, html

print("APP START")

from utils.io import load_excel_monthly

print("IO IMPORT OK")


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"

print("ANTES DE LEER EXCEL")

# df = load_excel_monthly(DATA_FILE)

print("DESPUES DE LEER EXCEL")


app = Dash(__name__)

app.layout = html.Div(
    "AthleteOS Render Test"
)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )