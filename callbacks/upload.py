import base64
import io
import pandas as pd
import dash_bootstrap_components as dbc

from dash import html, Input, Output, State, no_update
from utils.io import load_training_data

from core.engine import AthleteOSCore


def register_upload_callbacks(app):

    @app.callback(
        Output("uploaded-data-store", "data"),
        Output("upload-status", "children"),
        Input("upload-training-data", "contents"),
        State("upload-training-data", "filename"),
        prevent_initial_call=True
    )
    def upload_training_file(contents, filename):

        if contents is None:
            return no_update, ""

        try:

            content_type, content_string = contents.split(",")

            decoded = base64.b64decode(content_string)

            temp_file = io.BytesIO(decoded)
            temp_file.seek(0)

            df = load_training_data(temp_file)

            core = AthleteOSCore()

            prepared = core.prepare_data(df)

            squad = core.analyze_squad(prepared)

            priority = core.prioritize_squad(squad)

            return (
                {
                    "df": prepared.to_dict("records"),
                    "squad": squad.to_dict("records"),
                    "priority": priority.to_dict("records")
                },

                dbc.Alert(
                    [
                        html.B("✅ Archivo cargado correctamente"),
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