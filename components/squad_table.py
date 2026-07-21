import dash_bootstrap_components as dbc
from dash import html


STATUS_BADGES = {

    "Óptimo": "success",

    "Precaución": "warning",

    "Riesgo elevado": "danger",

    "Subentrenamiento": "primary"

}


def build_squad_table(squad):

    
    rows = []


    # Ordenamos por prioridad de intervención

    priority = {

        "Riesgo elevado": 1,

        "Precaución": 2,

        "Subentrenamiento": 3,

        "Óptimo": 4

    }


    squad = squad.copy()

    squad["priority"] = (
        squad["status"]
        .map(priority)
    )


    squad = (
        squad
        .sort_values("priority")
    )


    for _, row in squad.iterrows():

        rows.append(

            dbc.Card(

                [

                    dbc.CardBody(

                        [

                            dbc.Row(

                                [

                                    dbc.Col(

                                        html.H5(
                                            row["player"]
                                        ),

                                        width=3

                                    ),


                                    dbc.Col(

                                        [

                                            html.Small(
                                                "Carga"
                                            ),

                                            html.H5(
                                                row["daily_load"]
                                            )

                                        ],

                                        width=2

                                    ),


                                    dbc.Col(

                                        [

                                            html.Small(
                                                "ACWR"
                                            ),

                                            html.H5(
                                                row["acwr"]
                                            )

                                        ],

                                        width=2

                                    ),


                                    dbc.Col(

                                        dbc.Badge(

                                            row["status"],

                                            color=
                                            STATUS_BADGES[
                                                row["status"]
                                            ],

                                            className="p-2"

                                        ),

                                        width=2

                                    ),


                                    dbc.Col(

                                        html.Small(
                                            row["recommendation"]
                                        ),

                                        width=3

                                    )

                                ]

                            )

                        ]

                    )

                ],

                className="mb-2"

            )

        )


    return html.Div(rows)