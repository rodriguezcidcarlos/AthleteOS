from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


def build_executive_summary(df, squad):

    styles = getSampleStyleSheet()

    elements = []

    elements.append(PageBreak())

    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 0.7 * cm))

    # ==========================
    # Métricas
    # ==========================

    # Disponibilidad actual
    availability = round(
        squad["risk"]
        .apply(
            lambda x: isinstance(x, dict)
            and x.get("available", False)
        )
        .mean() * 100,
        1
    )

    # Último registro por jugador (mínimo 6 sesiones)
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

    # Métricas actuales
    acwr = round(latest["acwr"].mean(), 2)

    high = int(
        (latest["acwr"] > 1.30).sum()
    )
    # ==========================
    # Resumen
    # ==========================

    elements.append(
        Paragraph(
            "<b>Situación general</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 0.3 * cm))

    elements.append(
        Paragraph(
            f"La disponibilidad estimada de la plantilla es del <b>{availability}%</b>.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 0.2 * cm))

    elements.append(
        Paragraph(
            f"El ACWR medio actual es de <b>{acwr}</b>.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 0.2 * cm))

    elements.append(
        Paragraph(
            f"Se detectan <b>{high}</b> jugadores con exposición elevada (ACWR superior a 1.30).",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 0.7 * cm))

    elements.append(
        Paragraph(
            "<b>Puntos fuertes</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 0.3 * cm))

    elements.append(
        Paragraph(
            "• Seguimiento individualizado de la carga.",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "• Control continuo mediante EWMA y ACWR.",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "• Visualización rápida del estado de la plantilla.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 0.7 * cm))

    elements.append(
        Paragraph(
            "<b>Acciones prioritarias</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 0.3 * cm))

    elements.append(
        Paragraph(
            "• Reducir carga en jugadores con exposición elevada.",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "• Mantener la progresión en jugadores en rango óptimo.",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "• Reevaluar la situación tras las próximas sesiones.",
            styles["BodyText"]
        )
    )
    
    return elements