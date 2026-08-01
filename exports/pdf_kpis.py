from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet


def build_kpis(df, squad):

    total = len(squad)

    available = squad["risk"].apply(
        lambda r: isinstance(r, dict)
        and r.get("available", False)
    ).sum()

    high = squad["risk"].apply(
        lambda r: isinstance(r, dict)
        and r.get("level") == "Alto"
    ).sum()

    optimal = (
        squad["status"] == "Óptimo"
    ).sum()


    kpi_style = ParagraphStyle(
        "kpi",
        parent=getSampleStyleSheet()["Normal"],
        alignment=1,
        fontSize=11,
        leading=13,
        textColor=colors.white
    )


    data = [

        [

            Paragraph(
                f"<b>{total}</b><br/>Jugadores",
                kpi_style
            ),

            Paragraph(
                f"<b>{available}</b><br/>Disponibles",
                kpi_style
            ),

            Paragraph(
                f"<b>{optimal}</b><br/>Óptimos",
                kpi_style
            ),

            Paragraph(
                f"<b>{high}</b><br/>Riesgo Alto",
                kpi_style
            )

        ]

    ]


    table = Table(
        data,
        colWidths=[4.2*cm]*4,
        rowHeights=[1.8*cm]
    )


    table.setStyle(
        TableStyle(
            [

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,-1),
                    colors.HexColor("#1F2937")
                ),

                (
                    "TEXTCOLOR",
                    (0,0),
                    (-1,-1),
                    colors.white
                ),

                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "MIDDLE"
                ),

                (
                    "TOPPADDING",
                    (0,0),
                    (-1,-1),
                    4
                ),

                (
                    "BOTTOMPADDING",
                    (0,0),
                    (-1,-1),
                    4
                )

            ]
        )
    )


    return table