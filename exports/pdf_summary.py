from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    Table,
    TableStyle,
    Spacer
)


def build_summary(df, squad):

    total_players = len(squad)

    high = (
        squad["status"].eq("High").sum()
        if "status" in squad.columns
        else 0
    )

    moderate = (
        squad["status"].eq("Moderate").sum()
        if "status" in squad.columns
        else 0
    )

    low = (
        squad["status"].eq("Low").sum()
        if "status" in squad.columns
        else 0
    )

    data = [

        ["Indicador", "Valor"],

        ["Jugadores", total_players],

        ["Riesgo Alto", high],

        ["Riesgo Moderado", moderate],

        ["Riesgo Bajo", low],

        ["Registros", len(df)]

    ]

    table = Table(
        data,
        colWidths=[8 * cm, 5 * cm]
    )

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0D6EFD")),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#444444")),

                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F5F7FA")),

                ("ALIGN", (1, 1), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8)

            ]

        )

    )

    return [

        table,

        Spacer(
            1,
            0.8 * cm
        )

    ]