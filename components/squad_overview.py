import dash_bootstrap_components as dbc
from dash import html


STATUS_COLORS = {

    "Óptimo": "success",

    "Precaución": "warning",

    "Riesgo elevado": "danger",

    "Subentrenamiento": "primary"

}


def build_squad_overview(squad):

    total_players = len(squad)

    mean_acwr = round(
        squad["acwr"].mean(),
        2
    )

    mean_load = round(
        squad["daily_load"].mean(),
        0
    )


    status_count = (
        squad["status"]
        .value_counts()
        .to_dict()
    )


    cards = []


    for status, color in STATUS_COLORS.items():

        cards.append(

            dbc.Col(

                dbc.Card(

                    [

                        dbc.CardHeader(
                            status
                        ),

                        dbc.CardBody(

                            html.H3(

                                status_count.get(
                                    status,
                                    0
                                )

                            )

                        )

                    ],

                    color=color,

                    outline=True

                ),

                width=3

            )

        )


    return [

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(

                        [

                            dbc.CardHeader(
                                "Jugadores"
                            ),

                            dbc.CardBody(

                                html.H2(
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
                                "ACWR medio"
                            ),

                            dbc.CardBody(

                                html.H2(
                                    mean_acwr
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
                                "Carga media"
                            ),

                            dbc.CardBody(

                                html.H2(
                                    mean_load
                                )

                            )

                        ]

                    ),

                    width=4

                )

            ]

        ),

        html.Br(),

        html.H4(
            "Estado plantilla"
        ),

        dbc.Row(
            cards
        )

    ]