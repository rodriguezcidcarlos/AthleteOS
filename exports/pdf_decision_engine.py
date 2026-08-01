from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from exports.decision_engine import build_decision_engine


def build_pdf_decision_engine(df, squad):

    styles = getSampleStyleSheet()

    decision = build_decision_engine(
        df,
        squad
    )

    title = Paragraph(
        "<b>AthleteOS Decision Engine</b>",
        styles["Heading1"]
    )

    status = Paragraph(

        f"""
        <font color="{decision['color']}">
        <b>{decision['status']}</b>
        </font>
        """,

        styles["Title"]

    )

    summary = Paragraph(
        decision["summary"],
        styles["BodyText"]
    )

    recommendation = Paragraph(

        f"""
        <b>Recomendación</b><br/><br/>
        {decision["recommendation"]}
        """,

        styles["BodyText"]

    )

    card = Table(

        [

            [status],

            [summary],

            [recommendation]

        ],

        colWidths=[16*cm]

    )

    card.setStyle(

        TableStyle(

            [

                ("BOX",(0,0),(-1,-1),2,
                 colors.HexColor(decision["color"])),

                ("BACKGROUND",(0,0),(-1,0),
                 colors.HexColor("#F8FAFC")),

                ("BOTTOMPADDING",(0,0),(-1,-1),14),

                ("TOPPADDING",(0,0),(-1,-1),14),

                ("LEFTPADDING",(0,0),(-1,-1),16),

                ("RIGHTPADDING",(0,0),(-1,-1),16),

                ("ALIGN",(0,0),(-1,0),"CENTER"),

            ]

        )

    )

    return [

        Spacer(1,0.6*cm),

        title,

        Spacer(1,0.4*cm),

        card,

        Spacer(1,0.8*cm)

    ]