import dash_bootstrap_components as dbc
from dash import html


def build_kpi_cards(
    total,
    available,
    optimal,
    subtraining,
    overload,
    medium,
    high
):

    cards = [

        (
            "✔️ Disponibles",
            f"{available}/{total}",
            "success"
        ),

        (
            "🟢 Carga óptima",
            optimal,
            "success"
        ),

        (
            "🟦 Subentrenamiento",
            subtraining,
            "info"
        ),

        (
            "🟠 Sobrecarga",
            overload,
            "warning"
        ),

        (
            "🟡 Riesgo medio",
            medium,
            "warning"
        ),

        (
            "🔴 Riesgo alto",
            high,
            "danger"
        )

    ]


    return dbc.Row(

        [

            dbc.Col(

                dbc.Card(

                    dbc.CardBody(

                        [

                            html.H6(
                                title,
                                className="text-muted"
                            ),

                            html.H2(
                                value,
                                className=f"fw-bold text-{color}"
                            )

                        ]

                    ),

                    className="shadow-sm h-100"

                ),

                md=2

            )

            for title, value, color in cards

        ],

        className="mb-4"

    )