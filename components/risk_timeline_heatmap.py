import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from utils.decision_engine import evaluate_status

def build_risk_timeline_heatmap(df, selected_month=None):
    data = df.copy()

    data["date"] = pd.to_datetime(data["date"])

    if selected_month:

        data = data[
            data["date"].dt.strftime("%Y-%m") == selected_month
        ]

    data = data.sort_values(
        ["player", "date"]
    )

    dias = {
        "Mon": "Lun", "Tue": "Mar", "Wed": "Mié",
        "Thu": "Jue", "Fri": "Vie", "Sat": "Sáb", "Sun": "Dom"
    }

    data["date_label"] = (
        data["date"]
        .dt.strftime("%d %b")
    )
    print(
        data[
            [
                "player",
                "date",
                "acwr",
                "status"
            ]
        ].tail(50)
    )
    # -------------------------
    # Clasificación numérica
    # -------------------------

    status_map = {

        "Subentrenamiento": 0,

        "Óptimo": 1,

        "Precaución": 2,

        "Riesgo elevado": 3

    }



    # Estado calculado desde ACWR real
    data["risk_text"] = data["status"]



    # Conversión numérica para colores del heatmap
    data["risk_level"] = (
        data["risk_text"]
        .map(status_map)
        .fillna(1)
    )

    
    daily_status = (
        data
        .sort_values("date")
        .groupby(
            [
                "player",
                "date_label"
            ],
            as_index=False
        )
        .tail(1)
    )


    heatmap_data = daily_status.pivot(
        index="player",
        columns="date_label",
        values="risk_level"
    )


    heatmap_text = daily_status.pivot(
        index="player",
        columns="date_label",
        values="risk_text"
    )

    month_start = data["date"].min().replace(day=1)

    month_end = (
        month_start +
        pd.offsets.MonthEnd(1)
    )

    full_dates = pd.date_range(
        month_start,
        month_end,
        freq="D"
    )


    date_labels = [
        d.strftime("%d %b")
        for d in full_dates
    ]


    heatmap_data = heatmap_data.reindex(
        columns=date_labels
    )

    heatmap_text = heatmap_text.reindex(
        columns=date_labels
    )

    # Orden jugadores por último estado registrado

    print(
        data[
            data["player"].isin(
                [
                    "Jugador_06",
                    "Jugador_13"
                ]
            )
        ][
            [
                "player",
                "date",
                "acwr",
                "status",
                "risk_text",
                "risk_level"
            ]
        ].tail(20)
    )

    latest_status = (
        data
        .sort_values(
            ["player","date"]
        )
        .groupby("player")
        .tail(1)
        [
            [
                "player",
                "risk_level"
            ]
        ]
        .set_index("player")
    )


    heatmap_data = heatmap_data.loc[
        latest_status
        .sort_values(
            "risk_level",
            ascending=False
        )
        .index
    ]


    heatmap_text = heatmap_text.loc[
        heatmap_data.index
    ]


    fig = go.Figure(

        data=go.Heatmap(

            xgap=1,
            ygap=1,

            z=heatmap_data.values,

            x=heatmap_data.columns,
            y=heatmap_data.index,
            
            customdata=heatmap_text.values,

            hoverongaps=False,

            hovertemplate=
            "<b>%{y}</b><br>" +
            "Fecha: %{x}<br>" +
            "Estado: %{customdata}<extra></extra>",


            colorscale=[

                [0.0, "#1B4F72"],
                [0.249, "#1B4F72"],

                [0.25, "#196F3D"],
                [0.499, "#196F3D"],

                [0.50, "#B7950B"],
                [0.749, "#B7950B"],

                [0.75, "#922B21"],
                [1.0, "#922B21"]

            ],
            zmin=0,

            zmax=3,

            colorbar=dict(

                tickvals=[0,1,2,3],

                ticktext=[

                    "Baja exposición",

                    "Óptimo",

                    "Precaución",

                    "Riesgo elevado"

                ]

            )

        )

    )


    fig.update_layout(

        title="Evolución del estado de carga por jugador",
        height=max(500, len(heatmap_data.index) * 32),

        xaxis_title="Fecha",

        yaxis_title="Jugador",

        xaxis=dict(
            side="top",
            tickangle=-45
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        plot_bgcolor="#111827",

        paper_bgcolor="#111827",

        font=dict(
            color="white"
        )

    )


    return dcc.Graph(
        figure=fig,
        config={
            "displayModeBar": False
        }
    )