# ==========================
# AthleteOS Theme
# ==========================


STATUS_COLORS = {

    "Óptimo": "success",

    "Subentrenamiento": "info",

    "Riesgo elevado": "warning",

    "Alto": "danger",

    "Medio": "warning",

    "Bajo": "success"

}



APP_COLORS = {

    "primary": "#00b4d8",

    "background": "#080808",

    "card": "#151515",

    "text": "#f8fafc",

    "muted": "#9ca3af"

}



def metric_card(
    title,
    value,
    color="primary",
    icon=None,
    subtitle=None
):

    from dash import html
    import dash_bootstrap_components as dbc


    return dbc.Card(

        dbc.CardBody(

            [

                html.Div(

                    [

                        html.Span(
                            icon if icon else "",
                            className="me-2 fs-5"
                        ),

                        html.Small(
                            title,
                            className="text-muted text-uppercase fw-bold"
                        )

                    ],

                    className="d-flex align-items-center"

                ),


                html.H2(

                    value,

                    className=f"text-{color} fw-bold mt-3 mb-1"

                ),


                html.Small(

                    subtitle if subtitle else "",

                    className="text-secondary"

                )


            ],

            className="p-3"

        ),


        className=(

            "shadow-sm "
            "h-100 "
            "bg-dark "
            "border-secondary "
            "rounded-4"

        )

    )