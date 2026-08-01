from datetime import datetime
from exports.pdf_styles import (
    TITLE,
    SUBTITLE,
    BODY,
    LABEL,
)

from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from exports.pdf_theme import ACCENT, PRIMARY
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO = BASE_DIR / "assets" /"logo" / "athleteos_logo_white.png"

def build_cover(df, squad):

    story = []


    # ==========================================
    # Logo
    # ==========================================

    logo = Image(
        str(LOGO),
        width=12*cm,
        height=2.4*cm
    )

    logo.hAlign = "CENTER"

    story.append(logo)

    # ==========================================
    # Título
    # ==========================================

    story.append(
        Paragraph(
            "Executive Performance<br/>Report",
            TITLE
        )
    )
    

    story.append(
        Spacer(
            1,
            0.35 * cm
        )
    )

    story.append(
        Paragraph(
            "AthleteOS Performance Intelligence Platform",
            SUBTITLE
        )
    )


    story.append(
        Spacer(
            1,
            1.2 * cm
        )
    )


    # ==========================================
    # Línea corporativa
    # ==========================================

    line = Table(
        [[""]],
        colWidths=[17 * cm]
    )

    line.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    ACCENT
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    2
                ),
            ]
        )
    )

    story.append(line)


    story.append(
        Spacer(
            1,
            1 * cm
        )
    )


    # ==========================================
    # Información del informe
    # ==========================================

    info = [
        [
            Paragraph(
                "<b>Date</b>",
                LABEL
            ),
            Paragraph(
                datetime.now().strftime("%d %B %Y"),
                BODY
            )
        ],
        [
            Paragraph(
                "<b>Players analysed</b>",
                LABEL
            ),
            Paragraph(
                str(len(squad)),
                BODY
            )
        ],
        [
            Paragraph(
                "<b>Sessions analysed</b>",
                LABEL
            ),
            Paragraph(
                str(len(df)),
                BODY
            )
        ],
    ]


    table = Table(
        info,
        colWidths=[
            5 * cm,
            8 * cm
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,-1),
                    PRIMARY
                ),
                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "MIDDLE"
                ),
            ]
        )
    )

    story.append(table)


    story.append(
        Spacer(
            1,
            6 * cm
        )
    )


    story.append(
        Paragraph(
            "Generated automatically by AthleteOS",
            LABEL
        )
    )


    story.append(
        Spacer(
            1,
            0.3 * cm
        )
    )


    story.append(
        Paragraph(
            "CONFIDENTIAL",
            SUBTITLE
        )
    )



    return story