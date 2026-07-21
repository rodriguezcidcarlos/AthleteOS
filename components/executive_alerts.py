from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

def build_executive_alerts(squad, df):

    high = (
        squad["risk"]
        .apply(lambda x: x["level"] == "Alto")
        .sum()
    )

    medium = (
        squad["risk"]
        .apply(lambda x: x["level"] == "Medio")
        .sum()
    )

    available = (
        squad["risk"]
        .apply(lambda x: x["available"])
        .sum()
    )

    total = len(squad)

    # ==========================
    # Jugadores con ACWR elevado
    # Baseline mínimo 6 sesiones
    # ==========================

    sessions = (
        df[df["daily_load"] > 0]
        .groupby("player_id")
        .size()
    )


    valid_players = sessions[
        sessions >= 6
    ].index


    latest = (
        df[
            df["player_id"].isin(valid_players)
        ]
        .sort_values("date")
        .groupby("player_id")
        .tail(1)
    )


    if len(latest) > 0:

        high_acwr_players = int(
            (latest["acwr"] > 1.30)
            .sum()
        )

    else:

        high_acwr_players = 0

    # ==========================
    # Última actualización
    # ==========================

    last_date = pd.to_datetime(
        df["date"],
        errors="coerce"
    ).max()


    if pd.notna(last_date):

        last_update = last_date.strftime(
            "%d %b %Y"
        )

    else:

        last_update = "Sin fecha"

    return dbc.Row(

        [

            dbc.Col(

                dbc.Alert(

                    [

                        html.H4("⚠️"),

                        html.H5(
                            f"{high}"
                        ),

                        html.Small(
                            "Riesgo alto"
                        )

                    ],

                    color="danger",

                    className="text-center shadow-sm"

                ),

                md=3

            ),

            dbc.Col(

                dbc.Alert(

                    [

                        html.H4("⚡"),

                        html.H5(
                            f"{high_acwr_players}",
                        ),

                        html.Small(
                            "Jugadores ACWR elevado"
                        )

                    ],

                    color="warning",

                    className="text-center shadow-sm"

                ),

                md=3

            ),

            dbc.Col(

                dbc.Alert(

                    [

                        html.H4("✔️"),

                        html.H5(
                            f"{available}/{total}"
                        ),

                        html.Small(
                            "Disponibles"
                        )

                    ],

                    color="success",

                    className="text-center shadow-sm"

                ),

                md=3

            ),

            dbc.Col(

                dbc.Alert(

                    [

                        html.H4("🕒"),

                        html.H5(last_update),

                        html.Small(
                            "Última actualización"
                        )

                    ],

                    color="primary",

                    className="text-center shadow-sm"

                ),

                md=3

            )

        ],

        className="mb-4"

    )