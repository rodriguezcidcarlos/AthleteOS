import plotly.graph_objects as go
from dash import dcc
import dash_bootstrap_components as dbc


def build_executive_gauges(df, squad):


    # ==========================
    # Último estado individual
    # Jugadores con baseline suficiente
    # ==========================

    sessions = (
        df.groupby("player_id")
        .size()
    )


    valid_players = sessions[
        sessions >= 6
    ].index


    latest = (
        df[
            df["player_id"].isin(valid_players)
        ]
        .sort_values("date")
        .groupby("player_id")
        .tail(1)
    )

    # ==========================
    # ACWR medio actual plantilla
    # ==========================

    if len(latest) > 0:

        acwr = round(
            latest["acwr"].mean(),
            2
        )

    else:

        acwr = 0


    # ==========================
    # Disponibilidad
    # ==========================

    available = (
        squad["risk"]
        .apply(
            lambda x: x["available"]
        )
        .mean()
        *
        100
    )


    # ==========================
    # Exposición elevada
    # Jugadores con ACWR > 1.30
    # Baseline mínimo 6 sesiones
    # ==========================

    if len(latest) > 0:

        high_exposure = int(
            (latest["acwr"] > 1.30)
            .sum()
        )

    else:

        high_exposure = 0


    total_evaluated = len(latest)

    if total_evaluated > 0:

        exposure = round(
            (high_exposure / total_evaluated) * 100,
            1
        )

    else:

        exposure = 0
    
    def create_gauge(
        title,
        value,
        max_value,
        suffix="",
        gauge_type="acwr"
    ):

        # ==========================
        # Rangos específicos indicador
        # ==========================

        if gauge_type == "acwr":

            axis_range = [0, 2]

            steps = [

                {
                    "range":[0,0.80],
                    "color":"#1B2631"
                },

                {
                    "range":[0.80,1.30],
                    "color":"#145A32"
                },

                {
                    "range":[1.30,1.50],
                    "color":"#B7950B"
                },

                {
                    "range":[1.50,2],
                    "color":"#641E16"
                }

            ]


        elif gauge_type == "availability":

            axis_range = [0,100]

            steps = [

                {
                    "range":[0,33],
                    "color":"#641E16"
                },

                {
                    "range":[33,66],
                    "color":"#B7950B"
                },

                {
                    "range":[66,100],
                    "color":"#145A32"
                }

            ]


        elif gauge_type == "exposure":

            axis_range = [0,100]

            steps = [

                {
                    "range":[0,10],
                    "color":"#145A32"
                },

                {
                    "range":[10,25],
                    "color":"#B7950B"
                },

                {
                    "range":[25,100],
                    "color":"#641E16"
                }

            ]

        fig = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=value,

                title={
                    "text": title
                },

                number={
                    "suffix": suffix
                },

                gauge={

                    "axis":{
                        "range": axis_range
                    },

                    "bar":{
                    "color":"#FF9800"
                },

                    "steps": steps

                }

            )

        )


        fig.update_layout(

            height=250,

            margin=dict(
                l=30,
                r=30,
                t=70,
                b=30
            ),

            paper_bgcolor="#111827",

            font={
                "color":"white"
            }

        )


        return dcc.Graph(

            figure=fig,

            config={
                "displayModeBar":False
            }

        )


    return dbc.Row(

        [

            dbc.Col(

                create_gauge(
                    "ACWR Global",
                    acwr,
                    2,
                    gauge_type="acwr"
                ),

                width=4

            ),


            dbc.Col(

                create_gauge(
                    "Disponibilidad",
                    available,
                    100,
                    "%",
                    gauge_type="availability"
                ),

                width=4

            ),


            dbc.Col(

                create_gauge(
                    "Exposición elevada",
                    exposure,
                    100,
                    "%",
                    gauge_type="exposure"
                ),

                width=4

            )

        ],

        className="mb-4"

    )