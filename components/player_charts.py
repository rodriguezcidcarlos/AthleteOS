import plotly.graph_objects as go
from utils.plot_style import apply_athleteos_style
from dash import dcc
import dash_bootstrap_components as dbc

def interpret_acwr(acwr):

    if acwr < 0.8:
        return "Exposición inferior al rango recomendado"

    elif acwr < 1.3:
        return "Zona óptima de carga"

    elif acwr < 1.5:
        return "Incremento de carga reciente elevado"

    else:
        return "Zona de riesgo por sobrecarga"

def build_load_chart(player_df):

    fig = go.Figure()


    # ==========================
    # Carga diaria
    # ==========================

    fig.add_trace(

        go.Bar(

            x=player_df["date"],

            y=player_df["daily_load"],

            name="Carga diaria",

            opacity=0.35,

            hovertemplate=
            "<b>Fecha:</b> %{x}<br>" +
            "<b>Carga:</b> %{y}<extra></extra>"

        )

    )


    # ==========================
    # EWMA aguda
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=player_df["date"],

            y=player_df["acute_ewma"],

            mode="lines",

            name="EWMA Aguda (7d)",

            line=dict(
                width=3
            )

        )

    )


    # ==========================
    # EWMA crónica
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=player_df["date"],

            y=player_df["chronic_ewma"],

            mode="lines",

            name="EWMA Crónica (28d)",

            line=dict(
                width=3,
                dash="dash"
            )

        )

    )


    # ==========================
    # Último punto
    # ==========================

    last = player_df.iloc[-1]


    fig.add_trace(

        go.Scatter(

            x=[last["date"]],

            y=[last["daily_load"]],

            mode="markers",

            marker=dict(
                size=14,
                symbol="diamond"
            ),

            name="Última carga"

        )

    )


    # ==========================
    # Layout
    # ==========================

    fig.update_layout(


        height=350,

        hovermode="x unified",

        margin=dict(
            l=40,
            r=20,
            t=90,
            b=40
        ),

        legend=dict(
            orientation="h",
            y=1.15,
            x=0,
            xanchor="left",
            yanchor="bottom"
        )

    )


    fig = apply_athleteos_style(fig)


    return dbc.Card(

    [

        dbc.CardHeader(
            "📈 Evolución de carga"
        ),

        dbc.CardBody(

            dcc.Graph(
                figure=fig,
                config={
                    "displayModeBar": False
                }
            )

        )

    ],

     className="shadow-sm h-100 w-100"

)

def build_acwr_chart(player_df):

    fig = go.Figure()

    # ==========================
    # Bandas de riesgo
    # ==========================

    fig.add_hrect(
        y0=0,
        y1=0.80,
        fillcolor="#2563EB",
        opacity=0.20,
        line_width=0
    )

    fig.add_hrect(
        y0=0.80,
        y1=1.30,
        fillcolor="#22C55E",
        opacity=0.18,
        line_width=0
    )

    fig.add_hrect(
        y0=1.30,
        y1=1.50,
        fillcolor="#F59E0B",
        opacity=0.22,
        line_width=0
    )

    fig.add_hrect(
        y0=1.50,
        y1=2.50,
        fillcolor="#EF4444",
        opacity=0.20,
        line_width=0
    )

    # ==========================
    # Líneas de referencia
    # ==========================

    for y in [0.80, 1.30, 1.50]:

        fig.add_hline(
            y=y,
            line_dash="dash",
            line_color="gray",
            opacity=0.6
        )

    # ==========================
    # Línea ACWR
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=player_df["date"],
            y=player_df["acwr"],

            mode="lines+markers",

            name="ACWR",

            line=dict(
                width=4,
                color="#00b4d8"
            ),

            marker=dict(
                size=8
            ),

            customdata=player_df.assign(
                interpretation=player_df["acwr"].apply(
                    interpret_acwr
                )
            )[[
                "status",
                "daily_load",
                "interpretation"
            ]],

            hovertemplate=
            "<b>Fecha:</b> %{x}<br>" +
            "<b>ACWR:</b> %{y:.2f}<br>" +
            "<b>Estado:</b> %{customdata[0]}<br>" +
            "<b>Carga:</b> %{customdata[1]}<br>" +
            "<b>%{customdata[2]}</b><extra></extra>"

        )

    )

    # ==========================
    # Último entrenamiento
    # ==========================

    last = player_df.iloc[-1]
    
    fig.add_trace(

        go.Scatter(

            x=[last["date"]],
            y=[last["acwr"]],

            mode="markers",

            marker=dict(
            size=14,
            symbol="diamond"
        ),

            name="Estado actual"

        )

    )

    # ==========================
    # Layout
    # ==========================

    fig.update_layout(


        hovermode="x unified",

        height=350,

        margin=dict(
            l=40,
            r=20,
            t=90,
            b=40
        ),

        legend=dict(
            orientation="h",
            y=1.15,
            x=0,
            xanchor="left",
            yanchor="bottom"
        )

    )

    fig.update_yaxes(

        title="Carga externa",

        gridcolor="rgba(0,0,0,0.08)"

    )


    fig = apply_athleteos_style(fig)


    return dbc.Card(

        [

            dbc.CardHeader(
                "⚖️ Evolución ACWR"
            ),

            dbc.CardBody(

                dcc.Graph(
                    figure=fig,
                    config={
                        "displayModeBar": False
                    }
                )

            )

        ],

        className="mb-4 shadow-sm border-0 h-100"

    )
        

   