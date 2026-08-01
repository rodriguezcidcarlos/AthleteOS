from datetime import datetime

from exports.pdf_theme import *


def draw_footer(canvas, doc):

    width, _ = doc.pagesize

    canvas.saveState()

    # Línea separadora
    canvas.setStrokeColor(TEXT_LIGHT)

    canvas.line(
        30,
        35,
        width - 30,
        35
    )

    # Texto footer
    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.setFillColor(TEXT_LIGHT)

    canvas.drawString(
        35,
        20,
        "AthleteOS Performance Intelligence"
    )

    canvas.drawRightString(
        width - 35,
        20,
        f"Página {doc.page}"
    )

    # Fecha generación
    canvas.drawCentredString(
        width / 2,
        20,
        datetime.now().strftime("%d/%m/%Y")
    )

    canvas.restoreState()