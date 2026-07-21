import dash_bootstrap_components as dbc
from dash import html


def build_risk_card(risk):

    if not risk or not risk.get("available"):

        return dbc.Card(

            [

                dbc.CardHeader(
                    "Risk Intelligence",
                    className="py-2"
                ),

                dbc.CardBody(

                    [

                        html.H4(
                            "No disponible"
                        ),

                        html.P(
                            "Modelo predictivo no conectado."
                        )

                    ],

                    className="flex-grow-1"

                )

            ],

            className="h-100 w-100 shadow-sm d-flex flex-column"

        )


    level_colors = {

        "Bajo": "success",
        "Medio": "warning",
        "Alto": "danger"

    }


    color = level_colors.get(
        risk.get("level"),
        "secondary"
    )


    drivers = risk.get(
        "drivers",
        []
    )


    action = risk.get(
        "action",
        "Mantener seguimiento de evolución de carga."
    )


    print("DEBUG SCORE:", risk["score"])


    score = float(
        risk.get("score", 0)
    )


    score_percent = min(
        max(score * 100, 0),
        100
    )


    return dbc.Card(

        [

            dbc.CardHeader(
                "Risk Intelligence",
                className="py-2"
            ),


            dbc.CardBody(

                [

                    html.Div(

                        dbc.Badge(
                            risk["level"],
                            color=color,
                            className="fs-6 p-2"
                        ),

                        className="mb-4"

                    ),


                    html.H5(
                        "Índice de riesgo"
                    ),


                    html.H3(

                        f"{risk['score']:.2f} / 1.00",

                        className="text-primary"

                    ),


                    dbc.Progress(

                        value=score_percent,

                        max=100,

                        color=color,

                        striped=True,

                        className="mb-3"

                    ),


                    html.Small(

                        "Indicador compuesto de exposición basado en carga reciente, ACWR y desviación respecto al patrón individual. No representa una probabilidad clínica de lesión.",

                        className="text-muted d-block mb-4"

                    ),


                    html.H5(

                        "Factores detectados",

                        className="mt-4"

                    ),


                    html.Ul(

                        [

                            html.Li(driver)

                            for driver in drivers

                        ]

                    ),


                    html.H5(

                        "Interpretación",

                        className="mt-4"

                    ),


                    html.P(

                        risk.get(

                            "interpretation",

                            "El jugador requiere seguimiento según la evolución de carga."

                        )

                    ),


                    html.H5(

                        "Acción recomendada",

                        className="mt-4"

                    ),


                    dbc.Alert(

                        action,

                        color=color

                    )

                ],

                className="flex-grow-1"

            )

        ],

        className="h-100 w-100 shadow-sm d-flex flex-column"

    )