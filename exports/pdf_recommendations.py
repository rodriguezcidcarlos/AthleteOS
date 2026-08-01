from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from exports.pdf_styles import corporate_table_style


def build_recommendations(squad):

    styles = getSampleStyleSheet()

    elements = []


    elements.append(
        Paragraph(
            "Recomendaciones individuales",
            styles["Heading2"]
        )
    )


    elements.append(
        Spacer(
            1,
            0.3 * cm
        )
    )


    rows = [

        [
            "Jugador",
            "Hallazgo",
            "Recomendación"
        ]

    ]


    for _, row in squad.iterrows():

        player = row.get(
            "player",
            "-"
        )


        risk = row.get(
            "risk",
            {}
        )


        level = (
            risk.get("level", "-")
            if isinstance(risk, dict)
            else "-"
        )


        status = row.get(
            "status",
            "-"
        )


        if level == "Alto":

            finding = "Riesgo predictivo alto"

            action = (
                "Revisión individual y ajuste de carga."
            )


        elif level == "Medio":

            finding = "Riesgo predictivo medio"

            action = (
                "Mantener seguimiento preventivo."
            )


        elif status == "Subentrenamiento":

            finding = "Baja exposición"

            action = (
                "Incrementar progresivamente la carga."
            )


        elif status == "Sobrecarga":

            finding = "Carga elevada"

            action = (
                "Controlar volumen e intensidad."
            )


        else:

            finding = "Situación estable"

            action = (
                "Mantener planificación actual."
            )


        rows.append(
            [
                Paragraph(
                    player,
                    styles["BodyText"]
                ),

                Paragraph(
                    finding,
                    styles["BodyText"]
                ),

                Paragraph(
                    action,
                    styles["BodyText"]
                )
            ]
        )


    table = Table(
        rows,
        colWidths=[
            3.5 * cm,
            4.5 * cm,
            7 * cm
        ],
        repeatRows=1
    )


    table.setStyle(
        corporate_table_style()
    )


    elements.append(table)


    elements.append(
        Spacer(
            1,
            0.5 * cm
        )
    )


    return elements