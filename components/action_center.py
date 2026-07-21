from dash import html, dcc
import dash_bootstrap_components as dbc


def build_action_center(actions):

    if actions.empty:

        return html.P(
            "No existen acciones pendientes."
        )


    rows = []


    for _, row in actions.iterrows():

        risk = row["risk"]

        status = row["status"]

        risk_level = risk.get(
            "level",
            "Bajo"
        )


        # ==========================
        # Unificación de prioridad
        # ==========================

        if status == "Subentrenamiento":

            level = "Medio"

        elif risk_level == "Alto":

            level = "Alto"

        elif risk_level == "Medio":

            level = "Medio"

        else:

            level = "Bajo"


        risk_color = {

            "Alto": "danger",
            "Medio": "warning",
            "Bajo": "success"

        }.get(
            level,
            "secondary"
        )


        if level == "Alto":

            intervention = "Acción inmediata"
            intervention_color = "danger"

        elif level == "Medio":

            intervention = "Seguimiento"
            intervention_color = "warning"

        else:

            intervention = "Sin intervención"
            intervention_color = "success"


        if status == "Subentrenamiento":

            factor = (
                "ACWR bajo: exposición inferior al rango recomendado"
            )

        else:

            drivers = risk.get(
                "drivers",
                []
            )

            factor = (
                drivers[0]
                if drivers
                else
                "Sin factores detectados"
            )


        rows.append(

            html.Tr(

                [

                    html.Td(
                        row["player"]
                    ),

                    html.Td(
                        dbc.Badge(
                            level,
                            color=risk_color
                        )
                    ),

                    html.Td(
                        factor
                    ),

                    html.Td(
                        dbc.Badge(
                            intervention,
                            color=intervention_color
                        )
                    ),

                    html.Td(
                        risk.get(
                            "action",
                            "Mantener seguimiento"
                        )
                    ),

                    html.Td(

                        dbc.Button(
                            "Ver jugador",
                            id={
                                "type": "player-action",
                                "player_id": row["player_id"]
                            },
                            color="primary",
                            size="sm"
                        )

                    )

                ]

            )

        )

    # ==========================
    # Tabla final
    # ==========================

    table = dbc.Table(

        [

            html.Thead(

                html.Tr(

                    [

                        html.Th("Jugador"),
                        html.Th("Riesgo"),
                        html.Th("Factor principal"),
                        html.Th("Intervención"),
                        html.Th("Acción"),
                        html.Th("Detalle")

                    ]

                )

            ),

            html.Tbody(
                rows
            )

        ],

        bordered=True,
        hover=True,
        striped=True,
        responsive=True

    )


    return table