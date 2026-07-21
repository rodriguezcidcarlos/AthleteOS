print("000 APP START", flush=True)

from pathlib import Path

print("001 BEFORE DASH", flush=True)

from dash import Dash, html

print("002 DASH OK", flush=True)

from utils.io import load_excel_monthly

print("003 IO OK", flush=True)

from core.engine import AthleteOSCore

print("004 CORE IMPORT OK", flush=True)


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


print("005 BEFORE EXCEL", flush=True)

df = load_excel_monthly(DATA_FILE)

print("006 DATA OK", flush=True)
print(df.shape, flush=True)


# PARAMOS AQUÍ
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