import pandas as pd


REQUIRED_COLUMNS = [
    "player_id",
    "player",
    "date",
    "duration",
    "rpe",
]


def validate_training_data(df: pd.DataFrame) -> None:
    """
    Valida el DataFrame importado.

    Lanza ValueError si encuentra algún problema.
    """

    # ==========================
    # DataFrame vacío
    # ==========================
    if df.empty:
        raise ValueError(
            "El archivo no contiene registros."
        )

    # ==========================
    # Columnas obligatorias
    # ==========================
    missing = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Faltan las siguientes columnas: "
            + ", ".join(missing)
        )

    # ==========================
    # player_id
    # ==========================
    if df["player_id"].isna().any():
        raise ValueError(
            "Hay jugadores sin player_id."
        )

    # ==========================
    # player
    # ==========================
    if df["player"].isna().any():
        raise ValueError(
            "Hay jugadores sin nombre."
        )

    # ==========================
    # date
    # ==========================
    dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    if dates.isna().any():
        raise ValueError(
            "Hay fechas con formato incorrecto."
        )

    # ==========================
    # duration
    # ==========================
    duration = pd.to_numeric(
        df["duration"],
        errors="coerce"
    )

    if duration.isna().any():
        raise ValueError(
            "La columna 'duration' contiene valores no numéricos."
        )

    # ==========================
    # rpe
    # ==========================
    rpe = pd.to_numeric(
        df["rpe"],
        errors="coerce"
    )

    if rpe.isna().any():
        raise ValueError(
            "La columna 'rpe' contiene valores no numéricos."
        )