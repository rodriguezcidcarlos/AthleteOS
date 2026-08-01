from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from exports.pdf_theme import (
    PRIMARY,
    WHITE,
    BORDER,
)

from exports.pdf_header import draw_header
from exports.pdf_footer import draw_footer
from exports.pdf_cover import build_cover
from exports.pdf_kpis import build_kpis
from exports.pdf_table import build_executive_table
from exports.pdf_recommendations import build_recommendations
from exports.pdf_charts import build_pdf_charts
from exports.pdf_conclusions import build_conclusions

from exports.pdf_executive_summary import build_executive_summary
from exports.executive_insights import generate_executive_insights
from exports.pdf_score import build_score
from exports.pdf_trends import build_pdf_trends
from exports.pdf_decision_engine import build_pdf_decision_engine

from exports import pdf_fonts
from reportlab.platypus import KeepTogether

from exports.pdf_styles import corporate_table_style

from exports.pdf_compensatory import build_pdf_compensatory
from exports.pdf_compensatory import build_pdf_compensatory
from exports.pdf_md1_planning import build_pdf_md1_planning

def generate_pdf_report(
    df,
    squad,
    priority,
    figures,
    output_path
):

    insights = generate_executive_insights(
        df,
        squad
    )

    doc = SimpleDocTemplate(
        output_path,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=3.5 * cm,
        bottomMargin=1.8 * cm,
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==========================================
    # Portada
    # ==========================================

    elements.extend(
        build_cover(
            df,
            squad
        )
    )

    elements.extend(
        build_executive_summary(
            df,
            squad
        )
    )

    elements.extend(
        build_score(
            df,
            squad
        )
    )

    elements.append(
        Spacer(
            1,
            0.25 * cm
        )
    )

    elements.append(
        Paragraph(
            "Indicadores clave de rendimiento",
            styles["Heading2"]
        )
    )

    elements.append(
        build_kpis(
            df,
            squad
        )
    )


    elements.append(
        Paragraph(
            "Executive Insights",
            styles["Heading2"]
        )
    )
    
    elements.append(
        Spacer(
            1,
            0.3 * cm
        )
    )


    for insight in insights:

        elements.append(
            Paragraph(
                f"• {insight}",
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(
                1,
                0.08 * cm
            )
        )


    elements.extend(
        build_pdf_charts(
            figures
        )
        
    )
    elements.append(
        PageBreak()
    )

    
    # ==========================================
    # Recomendaciones individuales
    # ==========================================

    elements.extend(
        build_recommendations(
            squad
        )
    )

    # ==========================================
    # Action Center
    # ==========================================

    elements.append(
        PageBreak()
    )


    elements.append(
        Paragraph(
            "Centro de acciones prioritarias",
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
            "Riesgo",
            "Prioridad"
        ]
    ]


    if priority is not None and len(priority) > 0:

        for _, row in priority.iterrows():

            risk = row.get(
                "status",
                "-"
            )

            priority_value = row.get(
                "priority",
                "-"
            )


            if priority_value in [
                None,
                "",
                "nan"
            ]:
                priority_value = "-"


            rows.append(
                [
                    row.get(
                        "player",
                        "-"
                    ),

                    risk,

                    priority_value
                ]
            )


    else:

        rows.append(
            [
                "Sin datos",
                "-",
                "-"
            ]
        )


    priority_table = Table(
        rows,
        colWidths=[
            6 * cm,
            4 * cm,
            4 * cm
        ]
    )


    priority_table.setStyle(
        corporate_table_style()
    )

    elements.append(
        priority_table
    )

    
    # ==========================================
    # Monitorización plantilla
    # ==========================================

    elements.append(
        PageBreak()
    )
    

    elements.extend(
        build_pdf_trends(
            df
        )
    )

    elements.append(
        PageBreak()
    )

    elements.extend(
        build_pdf_md1_planning(
            df
        )
    )

    elements.append(
        PageBreak()
    )

    elements.extend(
        build_pdf_decision_engine(
            df,
            squad
        )
    )


    elements.append(
        PageBreak()
    )


    elements.extend(
        build_conclusions(
            df,
            squad
        )
    )

    # ==========================================
    # Construcción PDF
    # ==========================================

    def decorate_page(canvas, doc):

        draw_header(canvas, doc)
        draw_footer(canvas, doc)

    doc.build(
        elements,
        onFirstPage=decorate_page,
        onLaterPages=decorate_page
    )