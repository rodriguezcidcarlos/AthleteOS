import plotly.graph_objects as go


def build_acwr_trend_figure(df):

    trend = (
        df.groupby("date")["acwr"]
        .mean()
        .reset_index()
    )

    fig = go.Figure()

    # Zona óptima
    fig.add_hrect(
        y0=0.80,
        y1=1.30,
        fillcolor="green",
        opacity=0.12,
        line_width=0,
        layer="below"
    )

    # Evolución del ACWR
    fig.add_trace(
        go.Scatter(
            x=trend["date"],
            y=trend["acwr"],
            mode="lines+markers",
            line=dict(
                color="#FF9800",
                width=3
            ),
            marker=dict(
                size=7
            ),
            name="ACWR medio"
        )
    )

    # Último valor destacado
    fig.add_trace(
        go.Scatter(
            x=[trend["date"].iloc[-1]],
            y=[trend["acwr"].iloc[-1]],
            mode="markers+text",
            text=[f"{trend['acwr'].iloc[-1]:.2f}"],
            textposition="top center",
            marker=dict(
                size=12,
                color="#FF9800",
                line=dict(
                    color="white",
                    width=2
                )
            ),
            showlegend=False
        )
    )

    # Subentrenamiento
    fig.add_hline(
        y=0.80,
        line_dash="dash",
        line_color="#2563EB",
        annotation_text="Subentrenamiento",
        annotation_position="right"
    )

    # Alerta
    fig.add_hline(
        y=1.30,
        line_dash="dash",
        line_color="#D97706",
        annotation_text="Alerta",
        annotation_position="right"
    )

    # Riesgo
    fig.add_hline(
        y=1.50,
        line_dash="dash",
        line_color="#DC2626",
        annotation_text="Riesgo",
        annotation_position="right"
    )

    fig.update_layout(
        title="Evolución del ACWR medio de la plantilla",
        height=420,
        template="plotly_dark",
        xaxis_title="Fecha",
        yaxis_title="ACWR",
        yaxis=dict(
            range=[0.5, 1.7]
        ),
        hovermode="x unified",
        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40
        )
    )

    return fig