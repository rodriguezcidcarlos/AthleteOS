import pandas as pd


COLUMN_MAPPING = {
    "DÍA": "day",
    "DIA": "day",
    "FECHA": "date",
    "Fecha": "date",
    "JUGADOR": "player",
    "Jugador": "player",
    "ID_JUGADOR": "player_id",
    "ID Jugador": "player_id",
    "DURACIÓN": "duration",
    "Duración": "duration",
    "Duracion": "duration",
    "RPE": "rpe",
}


def normalize_columns(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    df.rename(
        columns=COLUMN_MAPPING,
        inplace=True
    )

    if "player" in df.columns:
        df["player"] = (
            df["player"]
            .astype(str)
            .str.strip()
        )

    for col in ["player_id", "day", "duration", "rpe"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df



def load_training_data(path):

    df = pd.read_excel(path)

    df = normalize_columns(df)

    if "date" not in df.columns and "day" in df.columns:

        df["date"] = pd.to_datetime(
            {
                "year": 2026,
                "month": 7,
                "day": df["day"]
            },
            errors="coerce"
        )

    return df