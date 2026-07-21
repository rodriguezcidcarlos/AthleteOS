from dash import Dash, html

print("ANTES DASH")

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