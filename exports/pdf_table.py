from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from exports.pdf_styles import corporate_table_style

def build_executive_table(squad, df):

    rows = [
        [
            "Jugador",
            "Riesgo",
            "Prioridad"
        ]
    ]

    for _, row in squad.iterrows():

        risk = "-"

        if isinstance(row.get("risk"), dict):
            risk = row["risk"].get(
                "level",
                "-"
            )

        priority = row.get(
            "priority",
            "-"
        )

        rows.append(
            [
                row.get("player", "-"),
                risk,
                priority
            ]
        )


    table = Table(
        rows,
        colWidths=[
            5 * cm,
            4 * cm,
            4 * cm
        ]
    )


    table.setStyle(
        corporate_table_style()
    )

    return table