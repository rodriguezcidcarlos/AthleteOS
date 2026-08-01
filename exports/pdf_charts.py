from reportlab.platypus import Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

import plotly.io as pio
import plotly.graph_objects as go

import tempfile
from pathlib import Path


def combine_gauges(figures):

    gauge_names = [
        "acwr",
        "availability",
        "exposure"
    ]

    combined = go.Figure()

    for i, name in enumerate(gauge_names):

        fig = figures[name]

        indicator = fig.data[0]

        combined.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=indicator.value,
                title=indicator.title,
                number=indicator.number,
                gauge=indicator.gauge,
                domain={
                    "x": [
                        i/3,
                        (i+1)/3
                    ],
                    "y": [
                        0,
                        1
                    ]
                }
            )
        )


    combined.update_layout(
        height=450,
        paper_bgcolor="white",
        font={
            "color":"black"
        },
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )


    return combined



def build_pdf_charts(figures):

    elements = []

    styles = getSampleStyleSheet()


    elements.append(
        Paragraph(
            "Indicadores visuales",
            styles["Heading2"]
        )
    )


    # ==========================
    # Gauges combinados
    # ==========================

    gauge_fig = combine_gauges(figures)


    gauge_path = (
        Path(tempfile.gettempdir())
        / "gauges.png"
    )


    pio.write_image(
        gauge_fig,
        str(gauge_path),
        width=1200,
        height=600
    )


    elements.append(
        Image(
            str(gauge_path),
            width=15*cm,
            height=7.5*cm
        )
    )

    elements.append(
        Spacer(
            1,
            0.25*cm
        )
    )


    # ==========================
    # Scatter exposición
    # ==========================

    if "scatter" in figures:

        scatter_path = (
            Path(tempfile.gettempdir())
            / "scatter.png"
        )


        pio.write_image(
            figures["scatter"],
            str(scatter_path),
            width=1000,
            height=550
        )


        elements.append(
            Image(
                str(scatter_path),
                width=15.5*cm,
                height=6.5*cm
            )
        )


    return elements