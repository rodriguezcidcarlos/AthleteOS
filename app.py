from pathlib import Path

from dash import Dash, html, dcc
from utils.io import load_excel_monthly, normalize_training_columns

print("IO IMPORT OK")


BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


df = load_excel_monthly(DATA_FILE)

print("DATA OK")
print(df.shape)
print(df.columns)


app = Dash(__name__)

print("DASH CREADO")


app.layout = html.Div(
    "AthleteOS Render Test"
)


print("LAYOUT OK")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )