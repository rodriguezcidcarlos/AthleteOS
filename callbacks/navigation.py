from dash import html, dcc, Input, Output
import pandas as pd

from components.import_data import build_import_data
from components.action_center import build_action_center
from components.squad_overview import build_squad_overview
from pages.executive_dashboard import build_executive_dashboard
import dash_bootstrap_components as dbc


def register_navigation_callbacks(app, df, squad):

    @app.callback(
        Output("page-content", "children"),
        Input("main-tabs", "active_tab"),
        Input("uploaded-data-store", "data")
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

                html.H2("Import Data"),

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