print("000 APP START")

from pathlib import Path
from dash import Dash, html

print("001 DASH OK")

from utils.io import load_training_data

print("002 IO OK")


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


print("003 BEFORE EXCEL")

df = load_training_data(DATA_FILE)

print("004 DATA OK")
print(df.shape)
print(df.columns)


app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("ATHLETEOS ONLINE 🚀"),
        html.H2("Render OK"),
        html.P(str(df.shape))
    ]
)