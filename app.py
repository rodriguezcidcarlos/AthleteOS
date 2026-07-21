from pathlib import Path

from dash import Dash, html

print("APP START")


from utils.io import load_excel_monthly

print("IO IMPORT OK")


from core.engine import AthleteOSCore

print("CORE IMPORT OK")


BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


print("ANTES DE LEER EXCEL")

df = load_excel_monthly(DATA_FILE)

print("DATA OK")
print(df.shape)


print("ANTES CORE")


core = AthleteOSCore(
    df
)

print("CORE INIT OK")


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