from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from exports.pdf_theme import (
    PRIMARY,
    ACCENT,
    TEXT,
    TEXT_LIGHT,
)


TITLE = ParagraphStyle(
    "Title",
    fontName="Azonix",
    fontSize=26,
    textColor=PRIMARY,
    alignment=TA_CENTER,
    leading=34,
    spaceAfter=24,
)


SUBTITLE = ParagraphStyle(
    "Subtitle",
    fontName="Montserrat",
    fontSize=12,
    textColor=TEXT_LIGHT,
    alignment=TA_CENTER,
    spaceAfter=16,
)


SECTION = ParagraphStyle(
    "Section",
    fontName="Montserrat-Bold",
    fontSize=18,
    textColor=PRIMARY,
    spaceBefore=12,
    spaceAfter=10,
)


ACCENT_SECTION = ParagraphStyle(
    "AccentSection",
    fontName="Montserrat-Bold",
    fontSize=14,
    textColor=ACCENT,
    spaceBefore=10,
    spaceAfter=8,
)


BODY = ParagraphStyle(
    "Body",
    fontName="Montserrat",
    fontSize=11,
    textColor=TEXT,
    leading=18,
    alignment=TA_LEFT,
)


METRIC = ParagraphStyle(
    "Metric",
    fontName="Montserrat-Bold",
    fontSize=24,
    textColor=PRIMARY,
    alignment=TA_CENTER,
)


LABEL = ParagraphStyle(
    "Label",
    fontName="Montserrat-SemiBold",
    fontSize=10,
    textColor=TEXT_LIGHT,
    alignment=TA_LEFT,
)

from reportlab.platypus import TableStyle
from exports.pdf_theme import (
    PRIMARY,
    WHITE,
    BORDER,
    TABLE_ALT_ROW,
    TABLE_TEXT
)


def corporate_table_style():

    return TableStyle(
        [

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                PRIMARY
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                WHITE
            ),

            (
                "FONTNAME",
                (0,0),
                (-1,0),
                "Helvetica-Bold"
            ),

            (
                "ROWBACKGROUNDS",
                (0,1),
                (-1,-1),
                [
                    "white",
                    TABLE_ALT_ROW
                ]
            ),

            (
                "TEXTCOLOR",
                (0,1),
                (-1,-1),
                TABLE_TEXT
            ),

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.25,
                BORDER
            ),

            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "MIDDLE"
            ),

            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            )


        ]
    )