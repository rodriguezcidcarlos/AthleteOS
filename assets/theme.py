# ======================================================
# AthleteOS Theme
# ======================================================

# =========================
# Identidad corporativa
# =========================

NAVY = "#020E2A"
PRIMARY = NAVY

SECONDARY = "#163A8A"
ACCENT = "#FF6B00"

# =========================
# Estados
# =========================

SUCCESS = "#16C784"
WARNING = "#F59E0B"
DANGER = "#DC2626"

# =========================
# Fondos
# =========================

BACKGROUND = "#F8FAFC"
CARD = "#FFFFFF"
HEADER = NAVY

# =========================
# Texto
# =========================

TEXT = "#1F2937"
TEXT_LIGHT = "#64748B"
TEXT_WHITE = "#F8FAFC"

# =========================
# Bordes
# =========================

BORDER = "#E5E7EB"
GRID = "#E2E8F0"

# =========================
# Tipografía
# =========================

FONT = "Montserrat"
TITLE = "Azonix"

# =========================
# Componentes
# =========================

RADIUS = 18
CARD_PADDING = "20px"

SHADOW = "0px 8px 24px rgba(2,14,42,0.10)"
HEADER_SHADOW = "0px 12px 30px rgba(2,14,42,0.18)"


# ======================================================
# Tema Plotly
# ======================================================

def athleteos_theme(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor=NAVY,
        plot_bgcolor=NAVY,

        font=dict(
            family=FONT,
            color=TEXT_WHITE,
            size=13
        ),

        title_font=dict(
            family=FONT,
            color=TEXT_WHITE,
            size=20
        ),

        xaxis=dict(
            gridcolor="#31405F",
            zeroline=False
        ),

        yaxis=dict(
            gridcolor="#31405F",
            zeroline=False
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )

    )

    return fig