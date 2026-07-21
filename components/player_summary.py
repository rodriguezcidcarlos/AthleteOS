import dash_bootstrap_components as dbc
from dash import html


def build_player_summary(analysis):

    status_colors = {
        "Óptimo": "success",
        "Precaución": "warning",
        "Riesgo elevado": "danger",
        "Subentrenamiento": "primary"
    }


    color = status_colors.get(
        analysis["status"],
        "secondary"
    )


    return dbc.Card(

        [

            dbc.CardHeader(
                "Análisis del jugador"
            ),


            dbc.CardBody(

                [

                    html.H4(
                        analysis["player"]
                    ),


                    html.H5(
                        [
                            "Estado: ",
                            dbc.Badge(
                                analysis["status"],
                                color=color
                            )
                        ]
                    ),


                    html.Hr(),


                    html.P(
                        f"ACWR actual: {analysis['acwr']}"
                    ),


                    html.P(
                        f"Tendencia carga: {analysis['trend']}"
                    ),


                    html.P(
                        f"Índice de carga: {analysis['load_index']:.2f}×"
                    ),


                    html.H5(
                        "Recomendación"
                    ),


                    html.P(
                        analysis["recommendation"]
                    )

                ]

            )

        ],

        className="h-100 w-100 shadow-sm"
    )