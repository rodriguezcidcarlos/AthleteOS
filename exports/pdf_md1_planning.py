from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from utils.compensatory import calculate_compensatory
from exports.pdf_styles import corporate_table_style
from reportlab.lib import colors

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

def build_pdf_md1_planning(df):

    styles = getSampleStyleSheet()
    
    header_style = styles["BodyText"].clone("table_header")
    header_style.textColor = colors.white
    header_style.fontName = "Helvetica-Bold"

    status_styles = {

        "Subentrenamiento": ParagraphStyle(
            "subtraining",
            parent=styles["BodyText"],
            textColor=colors.HexColor("#2563EB"),
            fontName="Helvetica-Bold"
        ),

        "Óptimo": ParagraphStyle(
            "optimal",
            parent=styles["BodyText"],
            textColor=colors.HexColor("#16A34A"),
            fontName="Helvetica-Bold"
        ),

        "Precaución": ParagraphStyle(
            "warning",
            parent=styles["BodyText"],
            textColor=colors.HexColor("#D97706"),
            fontName="Helvetica-Bold"
        ),

        "Riesgo elevado": ParagraphStyle(
            "danger",
            parent=styles["BodyText"],
            textColor=colors.HexColor("#DC2626"),
            fontName="Helvetica-Bold"
        )
    }

    comp_all = calculate_compensatory(df)

    if comp_all is None or comp_all.empty:
        return []

    # Resumen con toda la plantilla
    recovery = (
        comp_all["md1_minutes"] == 0
    ).sum()

    low = (
        (comp_all["md1_minutes"] > 0) &
        (comp_all["md1_minutes"] < 20)
    ).sum()

    medium = (
        (comp_all["md1_minutes"] >= 20) &
        (comp_all["md1_minutes"] < 45)
    ).sum()

    high = (
        comp_all["md1_minutes"] >= 45
    ).sum()


    # Solo mostrar los que trabajan MD+1
    comp = comp_all[
        comp_all["md1_minutes"] > 0
    ].copy()

    players_compensating = len(comp)

    summary_rows = [
        [
            Paragraph("Comp. baja", header_style),
            Paragraph("Comp. media", header_style),
            Paragraph("Comp. alta", header_style),
            Paragraph("Jugadores MD+1", header_style)
        ],
        [
            low,
            medium,
            high,
            players_compensating
        ]
    ]

    elements = []

    elements.append(
        Paragraph(
            "Planificación MD+1 - Trabajo compensatorio individual",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(1,0.3*cm)
    )
    
    
    comp = comp.sort_values(
        by="md1_minutes",
        ascending=False
    )
    
    rows = [
        [
            Paragraph("Jugador", header_style),
            Paragraph("Min partido", header_style),
            Paragraph("ACWR", header_style),
            Paragraph("Estado", header_style),
            Paragraph("Trabajo MD+1", header_style)
        ]
    ]

    for _, row in comp.iterrows():

        rows.append([

            Paragraph(
                row["player"],
                styles["BodyText"]
            ),

            row["minutes_played"],

            f"{row['acwr']:.2f}",
            
            Paragraph(
                row["status"],
                status_styles.get(
                    row["status"],
                    styles["BodyText"]
                )
            ),
            Paragraph(
                f"{row['md1_minutes']} min - {row['compensatory_work']}",
                styles["BodyText"]
            )

        ])


    summary_table = Table(
        summary_rows,
        colWidths=[
            3 * cm,
            3 * cm,
            3 * cm,
            4 * cm
        ],
        hAlign="CENTER"
    )

    summary_table.setStyle(
        corporate_table_style()
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.HexColor("#0F172A")
            ),
            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),
            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "MIDDLE"
            ),
            
            (
                "ALIGN",
                (3,1),
                (3,-1),
                "CENTER"
            )
        ])
    )


    elements.append(summary_table)

    elements.append(
        Spacer(
            1,
            0.5 * cm
        )
    )


    elements.append(
        Paragraph(
            "Planificación compensatoria automática basada en minutos disputados, estado ACWR y necesidad individual de completar carga MD+1.",
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 0.4 * cm)
    )


    table = Table(
        rows,
        colWidths=[
            2.8 * cm,   # Jugador
            1.8 * cm,     # Min partido
            1.8 * cm,   # ACWR
            4.5 * cm,     # Estado
            5.5 * cm      # Trabajo MD+1
        ],
        repeatRows=1,
        hAlign="CENTER"
    )


    table.setStyle(
        corporate_table_style()
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.HexColor("#0F172A")
            ),
            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),
            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "MIDDLE"
            ),
            
            (
                "BACKGROUND",
                (3,1),
                (3,-1),
                colors.HexColor("#EFF6FF")
            )
        ])
    )

    elements.append(table)
    return elements

    
    