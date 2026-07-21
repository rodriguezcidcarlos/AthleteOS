from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd

from core.engine import AthleteOSCore

from components.player_summary import build_player_summary
from components.risk_card import build_risk_card
from components.player_charts import (
    build_load_chart,
    build_acwr_chart
)

from styles import metric_card, STATUS_COLORS


def register_dashboard_callbacks(app):


    @app.callback(
        Output("dashboard-content", "children"),
        Input("player-selector", "value"),
        Input("uploaded-data-store", "data")
    )

    def update_dashboard(selected_player, store_data):

        if store_data is None:
            return html.Div(
                "Carga un archivo primero."
            )

        df = pd.DataFrame(
            store_data["df"]
        )


        if selected_player is None:

            return html.Div(
                "Selecciona un jugador."
            )

        try:
            selected_player = int(selected_player)

        except:
            return html.Div(
                "Jugador no válido."
            )

        player_df = df[
                df["player_id"] == selected_player
            ].copy()


        if player_df.empty:

            return html.Div(
                "No hay datos disponibles para este jugador."
            )


        # ==========================
        # Orden temporal correcto
        # ==========================

        player_df = (
            player_df
            .sort_values("date")
            .reset_index(drop=True)
        )


        last = player_df.iloc[-1]
    

        # ==========================
        # Análisis jugador
        # ==========================

        core = AthleteOSCore()

        analysis = core.analyze_player(
            player_df
        )



        risk_card = build_risk_card(
            analysis["risk"]
        )


        load_chart = build_load_chart(
            player_df
        )


        acwr_chart = build_acwr_chart(
            player_df
        )


        status = analysis.get(
            "status",
            "Sin clasificar"
        )


        status_color = STATUS_COLORS.get(
            status,
            "secondary"
        )


        return [


            html.H3(
                [
                    "👤 ",
                    last["player"]
                ],
                className="fw-bold text-primary mb-1"
            ),


            html.P(
                "Individual Performance Profile · Current Load Monitoring",
                className="text-secondary mb-3"
            ),



            # ==========================
            # KPIs superiores
            # ==========================

            dbc.Row(

                [

                    dbc.Col(

                        metric_card(
                            "ACWR",
                            round(last["acwr"], 2),
                            "info",
                            "⚡",
                            "Relación carga aguda/crónica"
                        ),

                        width=4

                    ),


                    dbc.Col(

                        metric_card(
                            "Estado",
                            status,
                            status_color,
                            "🏋️",
                            "Estado actual del jugador"
                        ),

                        width=4

                    ),


                    dbc.Col(

                        metric_card(
                            "Carga diaria",
                            int(last["daily_load"]),
                            "secondary",
                            "📈",
                            "Unidades de carga"
                        ),

                        width=4

                    )

                ],

                className="mb-4"

            ),



            html.Br(),



            # ==========================
            # Tarjetas principales
            # ==========================

            dbc.Row(

                [

                    dbc.Col(

                        build_player_summary(
                            analysis
                        ),

                        lg=6,
                        xs=12,
                        className="d-flex mb-3"

                    ),


                    dbc.Col(

                        risk_card,

                        lg=6,
                        xs=12,
                        className="d-flex mb-3"

                    )

                ],

                className="mb-4",
                align="stretch"

            ),



            load_chart,


            acwr_chart


        ]