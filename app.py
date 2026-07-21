print("000 APP START", flush=True)

from pathlib import Path

from dash import Dash, html

print("001 DASH OK", flush=True)

from utils.io import load_excel_monthly

print("002 IO OK", flush=True)


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


print("003 BEFORE EXCEL", flush=True)

df = load_excel_monthly(DATA_FILE)

print("004 DATA OK", flush=True)
print(df.shape, flush=True)


from core.engine import AthleteOSCore

print("005 CORE IMPORT OK", flush=True)


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