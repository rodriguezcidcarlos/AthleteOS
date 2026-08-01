from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


def build_insights(df, squad):

    styles = getSampleStyleSheet()

    total_players = len(squad)


    available = squad["risk"].apply(
        lambda r: isinstance(r, dict)
        and r.get("available", False)
    ).sum()


    high = squad["risk"].apply(
        lambda r: isinstance(r, dict)
        and r.get("level") == "Alto"
    ).sum()


    medium = squad["risk"].apply(
        lambda r: isinstance(r, dict)
        and r.get("level") == "Medio"
    ).sum()


    subtraining = (
        squad["status"] == "Subentrenamiento"
    ).sum()


    overload = (
        squad["status"] == "Sobrecarga"
    ).sum()


    if high > 0:

        situation = (
            f"Se detectan {high} jugador(es) con riesgo predictivo alto. "
            "Se recomienda revisión individual antes de modificar la carga."
        )

    elif medium > 0:

        situation = (
            f"Se identifican {medium} jugador(es) con riesgo predictivo medio. "
            "Mantener seguimiento preventivo."
        )

    else:

        situation = (
            "No se detectan niveles elevados de riesgo predictivo "
            "en la plantilla."
        )


    load = (
        f"La disponibilidad actual es de {available}/{total_players} jugadores. "
        f"El estado de carga muestra {subtraining} jugador(es) en "
        "subentrenamiento y "
        f"{overload} en sobrecarga."
    )


    elements = [

        Paragraph(
            "Executive Insights",
            styles["Heading2"]
        ),

        Spacer(
            1,
            0.3 * cm
        ),

        Paragraph(
            situation,
            styles["BodyText"]
        ),

        Spacer(
            1,
            0.2 * cm
        ),

        Paragraph(
            load,
            styles["BodyText"]
        ),

        Spacer(
            1,
            0.5 * cm
        )

    ]


    return elements