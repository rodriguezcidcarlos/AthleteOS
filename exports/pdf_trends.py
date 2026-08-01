from pathlib import Path
import tempfile

import plotly.io as pio

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Image,
    KeepTogether
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from components.trend_figures import build_acwr_trend_figure


def build_pdf_trends(df):

    styles = getSampleStyleSheet()

    elements = []

    fig = build_acwr_trend_figure(df)

    path = (
        Path(tempfile.gettempdir())
        / "acwr_trend.png"
    )

    pio.write_image(
        fig,
        str(path),
        width=1200,
        height=650
    )

    # =============================
    # Análisis de la plantilla
    # =============================

    last = (
        df.sort_values("date")
        .groupby("player")
        .last()
    )

    mean_acwr = last["acwr"].mean()

    under = (last["acwr"] < 0.80).sum()

    optimal = (
        (last["acwr"] >= 0.80) &
        (last["acwr"] < 1.30)
    ).sum()

    warning = (
        (last["acwr"] >= 1.30) &
        (last["acwr"] < 1.50)
    ).sum()

    danger = (
        last["acwr"] >= 1.50
    ).sum()

    trend = (
        df.groupby("date")["acwr"]
        .mean()
        .tail(5)
    )

    delta = trend.iloc[-1] - trend.iloc[0]

    if delta > 0.08:
        trend_text = "ascendente"

    elif delta < -0.08:
        trend_text = "descendente"

    else:
        trend_text = "estable"

    interpretation = []

    interpretation.append(
        f"• El ACWR medio de la plantilla es <b>{mean_acwr:.2f}</b>."
    )

    interpretation.append(
        f"• <b>{optimal}</b> jugadores ({optimal/len(last)*100:.0f}%) se encuentran dentro del rango óptimo de carga."
    )

    if under:
        interpretation.append(
            f"• <b>{under}</b> jugadores presentan un estado de subentrenamiento (ACWR < 0.80), por lo que podrían beneficiarse de un incremento progresivo de la carga."
        )

    if warning:
        interpretation.append(
            f"• <b>{warning}</b> jugadores se encuentran en zona de precaución (ACWR 1.30–1.50), recomendándose un seguimiento individual."
        )

    if danger:
        interpretation.append(
            f"• <b>{danger}</b> jugadores superan un ACWR de 1.50, lo que puede asociarse a un incremento del riesgo de sobrecarga."
        )

    interpretation.append(
        f"• La tendencia global del ACWR durante las últimas sesiones es <b>{trend_text}</b>."
    )

    # Valoración global de la plantilla
    if danger == 0 and warning == 0:
        interpretation.append(
            "• La distribución de cargas de la plantilla es homogénea y se mantiene dentro de parámetros adecuados."
        )

    elif danger == 0:
        interpretation.append(
            "• Aunque la mayoría de jugadores se encuentran en valores adecuados, conviene controlar la evolución de aquellos en zona de precaución."
        )

    else:
        interpretation.append(
            "• Se recomienda revisar individualmente la planificación de los jugadores con mayor exposición acumulada."
        )



    # ===========================
    # PDF
    # ===========================

    if danger >= 3:

        conclusion = (
            "La plantilla presenta una acumulación significativa de carga. "
            "Se recomienda reducir el volumen de trabajo de alta intensidad, "
            "priorizar la recuperación y monitorizar individualmente a los jugadores en riesgo."
        )

    elif under >= 5:

        conclusion = (
            "Se observa un número elevado de jugadores en subentrenamiento. "
            "Conviene incrementar progresivamente el estímulo de entrenamiento mediante trabajo complementario."
        )

    elif trend_text == "ascendente":

        conclusion = (
            "La carga global mantiene una evolución ascendente y se encuentra controlada. "
            "Es recomendable monitorizar la respuesta de la plantilla en las próximas sesiones."
        )

    elif trend_text == "descendente":

        conclusion = (
            "La carga de entrenamiento muestra una tendencia descendente, compatible con un periodo de recuperación o tapering."
        )

    else:

        conclusion = (
            "La distribución de cargas es equilibrada y la mayoría de la plantilla permanece dentro del rango óptimo de ACWR. "
            "La planificación prevista puede mantenerse sin modificaciones relevantes."
        )


    block = [

        Paragraph(
            "Tendencia de la plantilla",
            styles["Heading2"]
        ),

        Spacer(1,0.3*cm),

        Image(
            str(path),
            width=16*cm,
            height=7.5*cm
        ),

        Spacer(1,0.4*cm),

        Paragraph(
            "<b>Interpretación automática</b>",
            styles["Heading3"]
        ),

        Paragraph(
            "<br/>".join(interpretation),
            styles["BodyText"]
        ),

        Spacer(1,0.3*cm),

        Paragraph(
            "<b>Conclusión</b>",
            styles["Heading3"]
        ),

        Paragraph(
            conclusion,
            styles["BodyText"]
        )

    ]
    
    elements.append(
        KeepTogether(block)
    )

    return elements