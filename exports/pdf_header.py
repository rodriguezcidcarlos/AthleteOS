from pathlib import Path

from reportlab.lib.units import cm
from reportlab.platypus import Image

from exports.pdf_theme import PRIMARY, ACCENT, WHITE


BASE = Path(__file__).resolve().parent.parent

LOGO = BASE / "assets" / "logo" / "athleteos_logo.png"


def draw_header(canvas, doc):

    width, height = doc.pagesize

    # ==========================
    # Fondo principal
    # ==========================

    canvas.setFillColor(PRIMARY)

    canvas.rect(
        0,
        height - 2.4 * cm,
        width,
        2.4 * cm,
        fill=1,
        stroke=0,
    )


    # ==========================
    # Logo proporcional
    # ==========================

    logo = Image(str(LOGO))

    logo_width = 4.5 * cm
    aspect = logo.imageHeight / logo.imageWidth

    logo.drawWidth = logo_width
    logo.drawHeight = logo_width * aspect

    logo.wrapOn(
        canvas,
        width,
        height
    )

    logo.drawOn(
        canvas,
        1.5 * cm,
        height - 1.85 * cm,
    )


    # ==========================
    # Línea corporativa
    # ==========================

    canvas.setFillColor(ACCENT)

    canvas.rect(
        0,
        height - 2.45 * cm,
        width,
        0.08 * cm,
        fill=1,
        stroke=0,
    )


    # ==========================
    # Página
    # ==========================

    canvas.setFont(
        "Helvetica",
        9,
    )

    canvas.setFillColor(WHITE)

    canvas.drawRightString(
        width - 1.5 * cm,
        height - 1.2 * cm,
        f"Página {doc.page}",
    )