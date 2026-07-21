from dash import html
import dash_bootstrap_components as dbc
from components.kpi_cards import build_kpi_cards
from components.exposure_scatter import build_exposure_scatter
from components.action_ranking import build_action_ranking
from components.executive_alerts import build_executive_alerts
from components.executive_gauges import build_executive_gauges
from components.executive_table import build_executive_table

def build_executive_dashboard(squad, df):

        
    total = len(squad)


    available = squad["risk"].apply(
        lambda r: r["available"]
    ).sum()


    high = (
        squad["risk"]
        .apply(lambda r: r["level"] == "Alto")
        .sum()
    )

    medium = (
        squad["risk"]
        .apply(lambda r: r["level"] == "Medio")
        .sum()
    )

    low = (
        squad["risk"]
        .apply(lambda r: r["level"] == "Bajo")
        .sum()
    )

    subtraining = (
        squad["status"] == "Subentrenamiento"
    ).sum()

    optimal = (
        squad["status"] == "Óptimo"
    ).sum()

    overload = (
        squad["status"] == "Sobrecarga"
    ).sum()

    cards = build_kpi_cards(
        total,
        available,
        optimal,
        subtraining,
        overload,
        medium,
        high
    )

    alerts = build_executive_alerts(
        squad,
        df
    )

    gauges = dbc.Card(

        dbc.CardBody(

            build_executive_gauges(
                df,
                squad
            )

        ),

        className="mb-4 shadow-sm border-0"

    )

    scatter = build_exposure_scatter(
        df
    )
    
    print("PASO SCATTER EJECUTADO", flush=True)
    print(type(scatter), flush=True)

    actions = build_action_ranking(
        df
    )

    executive_table = build_executive_table(
        squad,
        df
    )
    
    
    
    # ==========================
    # Resumen ejecutivo
    # ==========================

    if high > 0:

        summary = (
            f"{high} jugador(es) presentan riesgo predictivo alto. "
            "Se recomienda revisión individual."
        )

    elif medium > 0:

        summary = (
            f"{medium} jugador(es) presentan riesgo predictivo medio. "
            "Mantener seguimiento individual."
        )

    else:

        summary = (
            "No se detectan niveles elevados de riesgo predictivo."
        )


    load_summary = (
        f"{subtraining} jugador(es) presentan subentrenamiento, "
        f"{optimal} mantienen exposición óptima y "
        f"{overload} presentan sobrecarga."
    )

    # ==========================
    # Tabla jugadores
    # ==========================

    rows = []


    for _, row in squad.iterrows():

        rows.append(

            html.Tr(

                [

                    html.Td(
                        row["player"]
                    ),

                    html.Td(
                        [
                            "🔴 " if row["risk"]["level"] == "Alto"
                            else
                            "🟡 " if row["risk"]["level"] == "Medio"
                            else
                            "🟢 ",
                            
                            row["risk"]["level"]
                        ]
                    ),

                    html.Td(

                        [
                            "🔴 " if row.get("priority") == "Alta"
                            else
                            "🟠 " if row.get("priority") == "Media"
                            else
                            "🟢 ",

                            row.get("priority", "-")
                        ]

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
                        html.Th("Estado"),
                        html.Th("Prioridad")

                    ]

                )

            ),

            html.Tbody(
                rows
            )

        ],

        bordered=True,

        hover=True,

        responsive=True

    )


    return dbc.Container(
        [

            html.H2(
                "Executive Performance Overview",
                className="fw-bold mb-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        cards,
                        width=12
                    )
                ],
                className="mb-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        alerts,
                        width=12
                    )
                ],
                className="mb-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                scatter
                            ),
                            className="shadow-sm border-0"
                        ),
                        width=12
                    )
                ],
                className="mb-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        gauges,
                        width=12
                    )
                ],
                className="mb-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        actions,
                        width=12
                    )
                ],
                className="mb-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Situación actual"),
                                    html.P(summary),
                                    html.Hr(),
                                    html.H6("Estado de carga"),
                                    html.P(load_summary)
                                ]
                            ),
                            className="shadow-sm border-0"
                        ),
                        width=12
                    )
                ],
                className="mb-4"
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H5(
                                        "Monitorización de plantilla (desviaciones relativas)",
                                        className="mb-1"
                                    )
                                ),

                                dbc.CardBody(
                                    executive_table
                                )
                            ],
                            className="shadow-sm"
                        ),
                        width=12
                    )
                ]
            )

        ],

        fluid=True
    )