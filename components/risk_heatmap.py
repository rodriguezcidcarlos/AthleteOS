import plotly.express as px
from dash import dcc
import plotly.graph_objects as go
from utils.decision_engine import evaluate_status

def build_risk_heatmap(squad):

    squad = squad.copy()


    # -------------------------
    # Variables riesgo
    # -------------------------

    squad["risk_score"] = squad["risk"].apply(
        lambda r: r["score"] if r["score"] is not None else 0
    )


    squad["risk_level"] = squad["risk"].apply(
        lambda r: r["level"]
    )


    squad["risk_factors"] = squad["risk"].apply(
        lambda r: "<br>".join(r["drivers"])
        if r["drivers"]
        else "Sin factores relevantes"
    )


    # -------------------------
    # Cuadrante fisiológico
    # -------------------------

    def classify_zone(row):

        acwr = row["acwr"]
        load = row["load_index"]


        if acwr < 0.8:

            return "Baja exposición crónica"


        elif acwr < 1.3 and load <= 1.2:

            return "Zona óptima"


        elif acwr < 1.5:

            return "Precaución"


        else:

            return "Riesgo elevado"


    squad["zone"] = squad.apply(
        classify_zone,
        axis=1
    )


    # -------------------------
    # Scatter jugadores
    # -------------------------

    fig = px.scatter(

        squad,

        x="load_index",

        y="acwr",

        color="zone",

        size="risk_score",

        text="player",

        hover_data={

            "player": True,

            "daily_load": True,

            "acwr": ":.2f",

            "load_index": ":.2f",

            "risk_level": True,

            "risk_score": ":.2f",

            "risk_factors": True

        },

        color_discrete_map={

            "Baja exposición crónica": "#5DADE2",

            "Zona óptima": "#58D68D",

            "Precaución": "#F4D03F",

            "Riesgo elevado": "#EC7063"

        },

        title="Matriz de Riesgo de Carga - Plantilla"

    )


    # -------------------------
    # Fondos cuadrantes
    # -------------------------

    fig.add_hrect(
        y0=0,
        y1=0.8,
        fillcolor="#5DADE2",
        opacity=0.12,
        line_width=0
    )


    fig.add_hrect(
        y0=0.8,
        y1=1.3,
        fillcolor="#58D68D",
        opacity=0.12,
        line_width=0
    )


    fig.add_hrect(
        y0=1.3,
        y1=1.5,
        fillcolor="#F4D03F",
        opacity=0.12,
        line_width=0
    )


    fig.add_hrect(
        y0=1.5,
        y1=2,
        fillcolor="#EC7063",
        opacity=0.12,
        line_width=0
    )


    # -------------------------
    # Límites ACWR
    # -------------------------

    for value, text in [

        (0.8, "Límite exposición"),

        (1.3, "Precaución"),

        (1.5, "Riesgo")

    ]:

        fig.add_hline(

            y=value,

            line_dash="dot",

            annotation_text=text,

            annotation_position="top left"

        )


    # -------------------------
    # Carga habitual
    # -------------------------

    fig.add_vline(

        x=1.2,

        line_dash="dash",

        annotation_text="Carga habitual"

    )


    fig.update_traces(
        textposition="top center"
    )


    fig.update_layout(

        height=650,

        xaxis_title="Índice de carga reciente",

        yaxis_title="ACWR",

        legend_title="Zona"

    )


    fig.update_xaxes(
        range=[
            0,
            max(3, squad["load_index"].max()*1.15)
        ]
    )


    fig.update_yaxes(
        range=[
            0,
            max(2, squad["acwr"].max()*1.15)
        ]
    )


    return dcc.Graph(
        figure=fig
    )