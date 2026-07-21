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

    print("IO 1 COPY", flush=True)

    df = df.copy()

    print("IO 2 CLEAN COLUMNS", flush=True)

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    print("IO 3 RENAME", flush=True)

    df.rename(
        columns=COLUMN_MAPPING,
        inplace=True
    )

    print("IO 4 PLAYER", flush=True)

    if "player" in df.columns:
        df.loc[:, "player"] = (
            df["player"]
            .astype(str)
            .str.strip()
        )

    print("IO 5 NUMERIC", flush=True)

    for col in ["player_id", "day", "duration", "rpe"]:

        if col in df.columns:

            print("CONVERT", col, flush=True)

            df.loc[:, col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    print("IO 6 RETURN", flush=True)

    return df



def load_training_data(path):

    print("LOAD 1 READ EXCEL", flush=True)

    df = pd.read_excel(path)

    print("LOAD 2 EXCEL OK", flush=True)
    print(df.shape, flush=True)

    df = normalize_columns(df)

    print("LOAD 3 NORMALIZED", flush=True)

    if "date" not in df.columns and "day" in df.columns:

        print("LOAD 4 DATE BUILD", flush=True)

        df["date"] = pd.to_datetime(
            {
                "year": 2026,
                "month": 7,
                "day": df["day"]
            },
            errors="coerce"
        )

    print("LOAD 5 RETURN", flush=True)

    return df