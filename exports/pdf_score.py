from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from exports.athleteos_score import calculate_athleteos_score


def build_score(df, squad):

    styles = getSampleStyleSheet()

    result = calculate_athleteos_score(
        df,
        squad
    )

    score = result["score"]
    
    if score >= 95:
        label = "ELITE"
        color = colors.HexColor("#16A34A")

    elif score >= 90:
        label = "EXCELENTE"
        color = colors.HexColor("#22C55E")

    elif score >= 80:
        label = "MUY BUENO"
        color = colors.HexColor("#65A30D")

    elif score >= 70:
        label = "BUENO"
        color = colors.HexColor("#F59E0B")

    elif score >= 60:
        label = "ATENCIÓN"
        color = colors.HexColor("#EA580C")

    else:
        label = "CRÍTICO"
        color = colors.HexColor("#DC2626")


    table = Table(
        [
            ["ATHLETEOS SCORE"],
            [f"{score:.1f}/100"],
            [label]
        ],
        colWidths=[12 * cm]
    )


    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0,0), (-1,-1), color),

                ("BOX", (0,0), (-1,-1), 1.5, color),

                ("ALIGN", (0,0), (-1,-1), "CENTER"),

                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

                ("TEXTCOLOR", (0,0), (-1,-1), colors.white),

                ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),

                ("FONTSIZE", (0,0), (-1,0), 12),

                ("FONTSIZE", (0,1), (-1,1), 26),

                ("FONTSIZE", (0,2), (-1,2), 14),

                ("TOPPADDING", (0,0), (-1,-1), 8),

                ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ]

        )
    )
        
    details = Table(

        [

            ["Disponibilidad", f'{result["availability"]}%'],

            ["ACWR medio", result["acwr"]],

            ["Exposición elevada", f'{result["exposure"]}%'],

            ["Riesgo predictivo", f'{result["risk"]}%']

        ],

        colWidths=[8*cm,4*cm]

    )

    details.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),0.25,colors.lightgrey),

                ("BOTTOMPADDING",(0,0),(-1,-1),8),

                ("TOPPADDING",(0,0),(-1,-1),8),

                ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F8FAFC")),

                ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

                ("ALIGN",(1,0),(1,-1),"CENTER")

            ]

        )

    )

    return [

        Paragraph(
            "AthleteOS Score",
            styles["Heading2"]
        ),

        Spacer(1,0.15*cm),

        table,

        Spacer(1,0.3*cm),

        details,

        Spacer(1,0.8*cm)

    ]