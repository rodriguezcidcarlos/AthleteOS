from dash import html, dcc
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd

def build_import_data():

    return dbc.Card(

    [

        dbc.CardHeader(
            "Import Data"
        ),

        dbc.CardBody(

            [

                html.P(
                    "Carga un archivo Excel de entrenamiento.",
                    className="text-muted"
                ),

                dcc.Upload(

                    id="upload-training-data",

                    children=html.Div(
                        [
                            "Arrastra un archivo aquí o ",
                            html.A("selecciona Excel")
                        ]
                    ),

                    style={
                        "width": "100%",
                        "height": "80px",
                        "lineHeight": "80px",
                        "borderWidth": "2px",
                        "borderStyle": "dashed",
                        "borderRadius": "10px",
                        "textAlign": "center"
                    },

                    multiple=False

                ),

                html.Br(),

                dbc.Button(

                    "Actualizar Dashboard",

                    id="update-dashboard-btn",

                    color="primary",

                    className="mt-2",

                    n_clicks=0

                ),

                html.Br(),
                html.Br(),

                html.Div(
                    id="upload-status"
                )

            ]

        )

    ],

    className="shadow-sm"

)
    