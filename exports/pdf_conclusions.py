from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


def build_conclusions(df, squad):

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Conclusiones ejecutivas",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(
            1,
            0.3 * cm
        )
    )

    conclusions = []
    
    available = (
        squad["risk"]
        .apply(
            lambda x: x.get("available", False)
            if isinstance(x, dict)
            else False
        )
        .mean()
        * 100
    )

    conclusions.append(
        f"• Disponibilidad estimada de la plantilla: <b>{available:.1f}%</b>."
    )
    
    high = (
        squad["risk"]
        .apply(
            lambda x: x.get("level", "")
            if isinstance(x, dict)
            else ""
        )
        .eq("Alto")
        .sum()
    )

    if high == 0:

        conclusions.append(
            "• No se detectan jugadores en riesgo predictivo alto."
        )

    else:

        conclusions.append(
            f"• Se identifican <b>{high}</b> jugadores con riesgo elevado."
        )
        
    exposed = (df["acwr"] > 1.30).sum()

    conclusions.append(
        f"• {exposed} registros presentan exposición elevada (ACWR > 1.30)."
    )
    
    if high == 0:

        text = (
            "• La situación general es estable. "
            "Se recomienda mantener la planificación actual "
            "y continuar la monitorización."
        )

    else:

        text = (
            "• Se recomienda revisar individualmente los jugadores "
            "priorizados y ajustar la carga cuando sea necesario."
        )

    conclusions.append(text)
    
    
    for c in conclusions:

        elements.append(
            Paragraph(
                c,
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(
                1,
                0.2 * cm
            )
        )

    return elements