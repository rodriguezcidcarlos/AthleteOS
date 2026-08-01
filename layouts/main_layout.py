from dash import html, dcc
import dash_bootstrap_components as dbc

from components.header import build_header


def build_main_layout(
    last_update,
    default_player,
    df,
    squad,
    priority
):

    return dbc.Container(

        [

            *build_header(last_update),

            dbc.Tabs(
                [
                    dbc.Tab(label="📊 Executive", tab_id="executive"),
                    dbc.Tab(label="👤 Jugador", tab_id="player"),
                    dbc.Tab(label="👥 Plantilla", tab_id="squad"),
                    dbc.Tab(label="🛠️ Action Center", tab_id="actions"),
                    dbc.Tab(label="📂 Import Data", tab_id="import"),
                ],
                id="main-tabs",
                active_tab="executive",
                className="mt-2"
            ),

            html.Br(),

            html.Div(id="page-content"),

            dcc.Store(
                id="athlete-data-store",
                data=None
            ),

            dcc.Store(
                id="uploaded-data-store",
                data={
                    "df": df.to_dict("records"),
                    "squad": squad.to_dict("records"),
                    "priority": priority.to_dict("records")
                }
            ),

            dcc.Store(
                id="selected-player",
                data=default_player
            ),
        

            dcc.Download(
                id="download-pdf"
            )

        ],

        fluid=True

    )