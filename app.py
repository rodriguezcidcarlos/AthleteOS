from pathlib import Path

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from layouts.main_layout import build_main_layout


from callbacks.navigation import register_navigation_callbacks
from callbacks.upload import register_upload_callbacks
from callbacks.player import register_player_callbacks
from callbacks.heatmap import register_heatmap_callbacks
from callbacks.export import register_export_callbacks
from components.dashboard import register_dashboard_callbacks

from services.bootstrap import initialize_data

from exports import pdf_fonts
from utils.match_detection import is_match_day


# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "synthetic_training.xlsx"


# ==========================
# Inicialización datos
# ==========================

(
    df,
    squad,
    priority,
    default_player,
    last_update,
) = initialize_data(DATA_FILE)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

server = app.server

app.title = "AthleteOS"

app.layout = build_main_layout(
    last_update,
    default_player,
    df,
    squad,
    priority
)
# ==========================
# Validación callbacks dinámicos
# ==========================

app.validation_layout = html.Div(

    [

        app.layout,

        dbc.Button(id="update-dashboard-btn"),

        dcc.Dropdown(id="risk-filter"),
        html.Div(id="action-center-container"),

        dcc.Dropdown(id="player-selector"),
        html.Div(id="dashboard-content"),

        dcc.Dropdown(id="month-selector"),
        html.Div(id="risk-calendar-container"),

    ]

)

# ==========================
# Registrar callbacks
# ==========================

register_navigation_callbacks(
    app,
    df,
    squad
)

register_dashboard_callbacks(
    app
)

register_upload_callbacks(
    app
)

register_player_callbacks(
    app,
    df,
    default_player
)

register_heatmap_callbacks(app)

register_export_callbacks(app)

# ==========================
# Ejecutar
# ==========================

if __name__ == "__main__":

    app.run(debug=True)