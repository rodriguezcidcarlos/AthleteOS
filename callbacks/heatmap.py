import pandas as pd
import dash_bootstrap_components as dbc

from dash import (
    html,
    Input,
    Output,
    State
)

from components.risk_timeline_heatmap import build_risk_timeline_heatmap


def register_heatmap_callbacks(app):
    
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
