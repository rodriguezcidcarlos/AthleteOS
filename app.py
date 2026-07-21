print("000 APP START", flush=True)

from pathlib import Path
from dash import Dash, html

print("001 DASH OK", flush=True)

import pandas as pd

print("002 PANDAS OK", flush=True)


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


print("003 BEFORE EXCEL", flush=True)

excel = pd.ExcelFile(DATA_FILE)

print("004 EXCEL OPEN OK", flush=True)

print(excel.sheet_names, flush=True)


df = pd.read_excel(
    DATA_FILE
)

print("005 READ OK", flush=True)

print(df.shape, flush=True)


app = Dash(__name__)

app.layout = html.Div(
    "AthleteOS Excel Test"
)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )