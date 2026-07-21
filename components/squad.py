from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


STATUS_ORDER = {
    "Riesgo elevado": 1,
    "Precaución": 2,
    "Subentrenamiento": 3,
    "Óptimo": 4
}


STATUS_COLORS = {
    "Óptimo": "success",
    "Precaución": "warning",
    "Riesgo elevado": "danger",
    "Subentrenamiento": "primary"
}


def create_squad_table(df: pd.DataFrame):

    # Último registro disponible de cada jugador

    latest = (
        df.sort_values("date")
        .groupby("player_id")
        .tail(1)
        .copy()
    )


    # Orden de prioridad

    latest["priority"] = (
        latest["status"]
        .map(STATUS_ORDER)
    )


    latest = (
        latest
        .sort_values(
            "priority"
        )
    )


    # Indicadores

    total_players = len(latest)

    risk_players = (
        latest["status"]
        .eq("Riesgo elevado")
        .sum()
    )

    undertraining_players = (
        latest["status"]
        .eq("Subentrenamiento")
        .sum()
    )


    rows = []


    for _, player in latest.iterrows():

        status = player["status"]


        rows.append(

            dbc.Row(

                [

                    dbc.Col(
                        player["player"],
                        width=3
                    ),


                    dbc.Col(
                        round(player["acwr"], 2),
                        width=2
                    ),


                    dbc.Col(

                        dbc.Badge(
                            status,
                            color=STATUS_COLORS[status],
                            className="p-2"
                        ),

                        width=3

                    ),


                    dbc.Col(
                        int(player["daily_load"]),
                        width=2
                    )

                ],

                className="border-bottom py-2"

            )

        )


    return [

        html.H2(
            "Estado de la plantilla"
        ),


        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Jugadores"
                            ),

                            dbc.CardBody(
                                html.H3(
                                    total_players
                                )
                            )
                        ]
                    ),

                    width=4

                ),


                dbc.Col(

                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Riesgo elevado"
                            ),

                            dbc.CardBody(
                                html.H3(
                                    risk_players
                                )
                            )
                        ]
                    ),

                    width=4

                ),


                dbc.Col(

                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Subentrenamiento"
                            ),

                            dbc.CardBody(
                                html.H3(
                                    undertraining_players
                                )
                            )
                        ]
                    ),

                    width=4

                )

            ]

        ),


        html.Br(),


        dbc.Row(

            [

                dbc.Col(
                    html.B("Jugador"),
                    width=3
                ),

                dbc.Col(
                    html.B("ACWR"),
                    width=2
                ),

                dbc.Col(
                    html.B("Estado"),
                    width=3
                ),

                dbc.Col(
                    html.B("Última carga"),
                    width=2
                )

            ],

            className="border-bottom"

        ),


        html.Br(),


        *rows

    ]