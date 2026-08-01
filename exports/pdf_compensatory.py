from reportlab.lib.units import cm
from reportlab.platypus import (
    Table,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import getSampleStyleSheet

from exports.pdf_styles import corporate_table_style
from utils.compensatory import calculate_compensatory


def build_pdf_compensatory(df):

    styles = getSampleStyleSheet()

    comp = calculate_compensatory(df)

    if comp is None:

        return []

    elements = []

    elements.append(
        Spacer(1,0.5*cm)
    )

    elements.append(
        Paragraph(
            "Compensatory Session (MD+1)",
            styles["Heading2"]
        )
    )

    elements.append(
        Spacer(1,0.3*cm)
    )

    rows = [[
        "Jugador",
        "Min.",
        "Carga",
        "Compensatorio"
    ]]

    for _, row in comp.iterrows():

        rows.append([
            row["player"],
            row["minutes_played"],
            row["match_load"],
            f'{row["comp_minutes"]} min'
        ])

    table = Table(
        rows,
        colWidths=[
            6*cm,
            2*cm,
            3*cm,
            4*cm
        ],
        repeatRows=1
    )

    table.setStyle(
        corporate_table_style()
    )

    elements.append(table)

    return elements