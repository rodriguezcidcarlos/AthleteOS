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


    df = df.rename(
        columns=COLUMN_MAPPING
    )


    if "player" in df.columns:

        df.loc[:, "player"] = (
            df["player"]
            .astype(str)
            .str.strip()
            .str.replace("\n", "", regex=False)
        )


    numeric_cols = [
        "player_id",
        "day",
        "duration",
        "rpe"
    ]


    for col in numeric_cols:

        if col in df.columns:

            df.loc[:, col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )


    return df

def load_training_data(path):

    df = pd.read_excel(path)


    df = normalize_columns(df)


    if "date" not in df.columns and "day" in df.columns:


        # Crear fecha sin pd.to_datetime
        df.loc[:, "date"] = pd.to_datetime(
            "2026-07-" +
            df["day"]
            .clip(lower=1, upper=31)
            .fillna(1)
            .astype(int)
            .astype(str)
            .str.zfill(2),
            errors="coerce"
        )


    return df