from dash import dcc
import dash_bootstrap_components as dbc
from dash import html


def build_action_ranking(df, selected_player=None):
    data = df.copy()

    if selected_player:

        data = data[
            data["player"] == selected_player
        ]

    # Último registro de cada jugador
    latest = (
        data.sort_values("date")
        .groupby("player")
        .tail(1)
        .copy()
    )


    # Prioridad automática

    def priority(row):

        if row["acwr"] >= 1.5:
            return "🔴 Alta"

        elif row["acwr"] >= 1.3:
            return "🟠 Media"

        elif row["acwr"] < 0.8:
            return "🔵 Progresión"

        else:
            return "🟢 Normal"


    latest["priority"] = latest.apply(
        priority,
        axis=1
    )


    # Acción recomendada

    def action(row):

        if row["acwr"] >= 1.5:

            return "Reducir exposición y revisar recuperación"

        elif row["acwr"] >= 1.3:

            return "Monitorizar evolución de carga"

        elif row["acwr"] < 0.8:

            return "Incrementar carga progresivamente"

        else:

            return "Mantener planificación"


    latest["action"] = latest.apply(
        action,
        axis=1
    )


    # Orden prioridad

    order = {
        "🔴 Alta":0,
        "🟠 Media":1,
        "🔵 Progresión":2,
        "🟢 Normal":3
    }


    latest["order"] = latest["priority"].map(order)


    latest = (
        latest
        .sort_values("order")
        .head(10)
    )


    rows=[]


    for _, r in latest.iterrows():

        rows.append(

            html.Tr(

                [

                    html.Td(
                        r["player"]
                    ),

                    html.Td(
                        f"{r['acwr']:.2f}"
                    ),

                    html.Td(
                        f"{r['chronic_ewma']:.0f}"
                    ),

                    html.Td(
                        r["status"]
                    ),

                    html.Td(
                        r["priority"]
                    ),

                    html.Td(
                        r["action"]
                    )

                ]

            )

        )


    table = dbc.Table(

        [

            html.Thead(

                html.Tr(

                    [

                        html.Th("Jugador"),
                        html.Th("ACWR"),
                        html.Th("Carga crónica"),
                        html.Th("Estado"),
                        html.Th("Prioridad"),
                        html.Th("Acción")

                    ]

                )

            ),

            html.Tbody(rows)

        ],

        bordered=True,

        hover=True,

        responsive=True,

        striped=True

    )


    return dbc.Card(

        [

            dbc.CardHeader(
                "🎯 Action Center - Prioridades actuales"
            ),

            dbc.CardBody(
                table
            )

        ],

        className="mt-4 shadow-sm"

    )