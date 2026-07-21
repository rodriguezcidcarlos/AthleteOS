import pandas as pd
import base64
import io
import pandas as pd

from dash import no_update
from components.action_center import build_action_center

from dash import Dash, html, dcc, Input, Output, State
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc

print("APP START")

import pandas as pd
print("PANDAS OK", pd.__version__)

import numpy as np
print("NUMPY OK", np.__version__)

from config import DATA_FILE

from utils.io import load_excel_monthly, normalize_training_columns
from core.engine import AthleteOSCore


from components.dashboard import register_dashboard_callbacks
from components.squad_table import build_squad_table
from components.squad_overview import build_squad_overview

from components.risk_heatmap import build_risk_heatmap
from components.risk_timeline_heatmap import build_risk_timeline_heatmap

from components.executive_dashboard import build_executive_dashboard
from components.import_data import build_import_data

from datetime import datetime

from utils.io import (
    load_training_data,
    load_uploaded_training_data,
    load_excel_monthly,
    normalize_training_columns
)
# Cargar datos
# ==========================

df = load_excel_monthly(DATA_FILE)

df = normalize_training_columns(df)

last_session = pd.to_datetime(
    df["date"]
).max().strftime("%d %b %Y")

last_update = datetime.now().strftime("%d %b %Y · %H:%M")

core = AthleteOSCore()

prepared = core.prepare_data(
    df
)

squad = core.analyze_squad(
    prepared
)

required = [
    "date",
    "player",
    "duration",
    "rpe"
]


missing = [
    c for c in required
    if c not in df.columns
]


if missing:

    raise ValueError(
        f"Faltan columnas necesarias: {missing}"
    )

df = core.prepare_data(df)

print(squad.iloc[0]["risk"])


# ==========================
# Jugadores
# ==========================

players = (
    df[
        [
            "player_id",
            "player"
        ]
    ]
    .drop_duplicates()
)


default_player = players["player_id"].iloc[0]


# ==========================
# Crear aplicación
# ==========================

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY
    ],
    suppress_callback_exceptions=True
)

server = app.server

app.title = "AthleteOS"

# ==========================
# Layout
# ==========================

app.layout = dbc.Container(

    [

        dbc.Row(

            [

                dbc.Col(

                    [

                        html.H1(
                            "AthleteOS",
                            className="display-4 fw-bold text-primary mb-0"
                        ),

                        html.P(
                            "Performance Intelligence Platform",
                            className="text-secondary fs-5 mb-0"
                        )

            
                    ],
                    
                    width=10,
                    className="d-flex flex-column justify-content-center"

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.Small(
                                    "🟢 Sistema online",
                                    className="text-success fw-bold"
                                ),

                                html.Hr(className="my-2"),

                                html.Small(
                                    "Última actualización",
                                    className="text-muted"
                                ),

                                html.Div(
                                    last_update,
                                    className="fw-bold mt-1"
                                )

                            ],

                            className="py-2 px-3"

                        ),

                        className="shadow-sm border-0 rounded-3",
                        style={
                            "maxWidth": "220px",
                            "marginLeft": "auto"
                        }

                    ),

                    width=2

                )

                            ],

                            className="mt-4 mb-3 align-items-center"

                        ),
            html.Hr(),
            html.Br(),
            
        dbc.Tabs(
            [

                dbc.Tab(
                    label="📊 Executive",
                    tab_id="executive"
                ),

                dbc.Tab(
                    label="👤 Jugador",
                    tab_id="player"
                ),

                dbc.Tab(
                    label="👥 Plantilla",
                    tab_id="squad"
                ),

                dbc.Tab(
                    label="🛠️ Action Center",
                    tab_id="actions"
                ),

                dbc.Tab(
                    label="📂 Import Data",
                    tab_id="import"
                ),

            ],

            id="main-tabs",
            active_tab="executive",
            className="mt-2"
        ),

        html.Br(),

      
        html.Div(
            id="page-content"
        ),

        dcc.Store(
            id="athlete-data-store",
            data=None
        ),

        dcc.Store(
            id="uploaded-data-store",
            data=None
        ),

        dcc.Store(
            id="selected-player",
            data=default_player
        )

    ],

    fluid=True
)
# ==========================
# Validación callbacks dinámicos
# ==========================

app.validation_layout = html.Div(
[
    app.layout,

    dbc.Button(
        id="update-dashboard-btn"
    ),

    # Action Center
    dcc.Dropdown(
        id="risk-filter"
    ),

    html.Div(
        id="action-center-container"
    ),


    # Jugador
    dcc.Dropdown(
        id="player-selector"
    ),

    html.Div(
        id="dashboard-content"
    ),


    # Heatmap calendario
    dcc.Dropdown(
        id="month-selector"
    ),

    html.Div(
        id="risk-calendar-container"
    )

]
)


# ==========================
# Navegación principal
# ==========================

@app.callback(
    Output("page-content","children"),
    Input("main-tabs","active_tab"),
    Input("uploaded-data-store","data")
)

def change_page(tab, store_data):

   
    # ==========================
    # Importar Datos
    # ==========================
    
    global df_current
    global squad_current


    if store_data:

        df_current = pd.DataFrame(
            store_data["df"]
        )

        squad_current = pd.DataFrame(
            store_data["squad"]
        )


    else:

        df_current = df
        squad_current = squad
    
    if tab == "import":

        return [

            html.H2(
                "Import Data"
            ),

            build_import_data()

        ]

    # ==========================
    # Executive Dashboard
    # ==========================

    if tab == "executive":

        return [

            build_executive_dashboard(
                squad_current,
                df_current
            )

        ]


    # ==========================
    # Plantilla
    # ==========================

    if tab == "squad":

        return [

            html.H2(
                "Squad Overview"
            ),

            *build_squad_overview(
                squad_current
            ),

            html.Br(),

            html.H2(
                "Evolución del riesgo"
            ),


            dcc.Dropdown(
                id="month-selector",
                options=[
                    {
                        "label": month.strftime("%B %Y"),
                        "value": month.strftime("%Y-%m")
                    }

                    for month in pd.date_range(
                        pd.to_datetime(df_current["date"]).min(),
                        pd.to_datetime(df_current["date"]).max(),
                        freq="MS"
                    )
                ],

                value=pd.to_datetime(
                    df_current["date"]
                ).min().strftime("%Y-%m"),

                clearable=False
            ),


            html.Br(),


            html.Div(
                id="risk-calendar-container"
            )

        ]


    # ==========================
    # Action Center
    # ==========================

    if tab == "actions":

        return [

            html.H2("Action Center"),

            html.P(
                "Priorización automática basada en carga, ACWR y evolución individual.",
                className="text-muted"
            ),

            html.Div(
                id="action-center-container",
                children=build_action_center(
                    squad_current
                )
            )

        ]

    # ==========================
    # Jugador
    # ==========================

    if tab == "player":

        return [

            html.H4(
                "Dashboard individual"
            ),

            html.P(
                "Selecciona un jugador para visualizar carga, ACWR y riesgo."
            ),

            dcc.Dropdown(

                id="player-selector",

                options=[
                    {
                        "label": row["player"],
                        "value": row["player_id"]
                    }
                    for _, row in squad_current.iterrows()
                ],

                clearable=False

            ),

            html.Br(),

            html.Div(
                id="dashboard-content"
            )

        ]
    return []        

# ==========================
# Actualizar selector jugador
# ==========================
 
@app.callback(
    Output("player-selector", "value"),
    Input("selected-player", "data"),
    State("uploaded-data-store", "data")
)
def update_player_selector(player_id, store_data):

    if store_data is None:
        return None

    squad = pd.DataFrame(
        store_data["squad"]
    )

    if player_id in squad["player_id"].values:
        return player_id

    return int(
        squad.iloc[0]["player_id"]
    )

# ==========================
# Abrir jugador desde Action Center
# ==========================

@app.callback(
    Output("main-tabs", "active_tab"),
    Output("selected-player", "data"),

    Input(
        {
            "type": "player-action",
            "player_id": ALL
        },
        "n_clicks"
    ),

    State(
        {
            "type": "player-action",
            "player_id": ALL
        },
        "id"
    ),

    prevent_initial_call=True
)
def open_player_from_action_center(clicks, ids):

    for click, item in zip(clicks, ids):

        if click:

            return (
                "player",
                item["player_id"]
            )

    return (
        "actions",
        default_player
    )


@app.callback(

    Output(
        "uploaded-data-store",
        "data"
    ),

    Output(
        "upload-status",
        "children"
    ),

    Input(
        "upload-training-data",
        "contents"
    ),

    State(
        "upload-training-data",
        "filename"
    ),

    prevent_initial_call=True

)
def upload_training_file(contents, filename):

    if contents is None:

        return no_update, ""


    try:

        content_type, content_string = contents.split(",")


        decoded = base64.b64decode(
            content_string
        )


        temp_file = io.BytesIO(decoded)


        temp_file.seek(0)

        df_import = pd.ExcelFile(
            temp_file
        )

        frames = []

        for sheet in df_import.sheet_names:

            df_month = pd.read_excel(
                temp_file,
                sheet_name=sheet
            )

            df_month["month"] = sheet

            frames.append(df_month)


        df_import = pd.concat(
            frames,
            ignore_index=True
        )


        df_import = load_uploaded_training_data(
            df_import
        )

        core = AthleteOSCore()

        prepared = core.prepare_data(df_import)

        squad = core.analyze_squad(prepared)

        
        
        return (

            {
                "df": prepared.to_dict("records"),

                "squad": squad.to_dict("records")
            },


            dbc.Alert(

                [

                    html.B(
                        "✅ Archivo cargado correctamente"
                    ),

                    html.Br(),

                    f"Archivo: {filename}",

                    html.Br(),

                    f"Registros: {len(prepared)}",

                    html.Br(),

                    f"Jugadores: {len(squad)}",

                    html.Br(),

                    f"Última fecha: {prepared['date'].max().strftime('%d %b %Y')}"

                ],

                color="success"

            )

        )


    except Exception as e:

        return (

            no_update,

            dbc.Alert(
                f"❌ Error al importar: {e}",
                color="danger"
            )

        )


# ==========================
# Registrar dashboard jugador
# ==========================

register_dashboard_callbacks(
    app
)

# ==========================
# Callback asociado al heatmap
# ==========================

@app.callback(
    Output(
        "risk-calendar-container",
        "children"
    ),

    Input(
        "month-selector",
        "value"
    ),

    State(
        "uploaded-data-store",
        "data"
    )
)
def update_risk_calendar(month, store_data):

    if store_data is None:

        return html.Div(
            "Carga un archivo primero."
        )


    df_heatmap = pd.DataFrame(
        store_data["df"]
    )


    heatmap = build_risk_timeline_heatmap(
        df_heatmap,
        selected_month=month
    )


    return dbc.Card(

        [

            dbc.CardHeader(
                "Risk Timeline"
            ),

            dbc.CardBody(
                heatmap
            )

        ],

        className="shadow-sm bg-dark text-white"

    )


# ==========================
# Ejecutar
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )