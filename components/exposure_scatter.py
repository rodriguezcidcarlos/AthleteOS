import plotly.graph_objects as go
from dash import dcc


def build_exposure_scatter(df):

    data = df.copy()

    # Último registro disponible de cada jugador
    latest = (
        data.sort_values("date")
        .groupby("player")
        .tail(1)
    )


    color_map = {
        "Subentrenamiento": "#3498DB",
        "Óptimo": "#2ECC71",
        "Precaución": "#F1C40F",
        "Riesgo elevado": "#E74C3C"
    }


    fig = go.Figure()


    for status in latest["status"].unique():

        subset = latest[
            latest["status"] == status
        ]


        fig.add_trace(

            go.Scatter(

                x=subset["acwr"],

                y=subset["chronic_ewma"],


                mode="markers+text",

                text=subset["player"],

                textposition="top center",


                name=status,


                marker=dict(

                    size=subset["daily_load"] / 8 + 10,

                    color=color_map.get(
                        status,
                        "gray"
                    ),

                    opacity=0.85,

                    line=dict(
                        width=1,
                        color="white"
                    )

                ),


                hovertemplate=

                "<b>%{text}</b><br>" +

                "ACWR: %{x:.2f}<br>" +

                "Carga crónica: %{y:.1f}<br>" +

                "Última carga: %{customdata}<br>" +

                "<extra></extra>",


                customdata=subset["daily_load"]

            )

        )


    # Zonas ACWR

    fig.add_vrect(
        x0=0,
        x1=0.8,
        fillcolor="#3498DB",
        opacity=0.08,
        line_width=0
    )


    fig.add_vrect(
        x0=0.8,
        x1=1.3,
        fillcolor="#2ECC71",
        opacity=0.08,
        line_width=0
    )


    fig.add_vrect(
        x0=1.3,
        x1=1.5,
        fillcolor="#F1C40F",
        opacity=0.10,
        line_width=0
    )


    fig.add_vrect(
        x0=1.5,
        x1=2,
        fillcolor="#E74C3C",
        opacity=0.10,
        line_width=0
    )


    for x in [0.8,1.3,1.5]:

        fig.add_vline(

            x=x,

            line_dash="dash",

            line_color="gray"

        )


    fig.update_layout(

        title="Mapa de exposición de plantilla",

        height=550,

        template="plotly_dark",

        xaxis=dict(

            title="ACWR actual",

            range=[
                0,
                max(2, latest["acwr"].max()*1.15)
            ]

        ),


        yaxis=dict(

            title="Carga crónica (EWMA 28 días)"

        ),


        hovermode="closest"

    )

    print("SCATTER TYPE:", type(fig), flush=True)
    
    return dcc.Graph(

        figure=fig,

        config={
            "displayModeBar": False
        }

    )