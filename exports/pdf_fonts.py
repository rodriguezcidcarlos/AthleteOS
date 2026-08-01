from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

FONT_DIR = BASE / "assets" / "fonts"

pdfmetrics.registerFont(
    TTFont(
        "Montserrat",
        str(FONT_DIR / "Montserrat-Regular.ttf")
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Montserrat-Bold",
        str(FONT_DIR / "Montserrat-Bold.ttf")
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Montserrat-SemiBold",
        str(FONT_DIR / "Montserrat-SemiBold.ttf")
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Azonix",
        str(FONT_DIR / "azonix.ttf")  
    )
)

from reportlab.pdfbase.pdfmetrics import registerFontFamily

registerFontFamily(
    "Montserrat",
    normal="Montserrat",
    bold="Montserrat-Bold",
    italic="Montserrat",
    boldItalic="Montserrat-Bold"
)

