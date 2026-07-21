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

    df = df.rename(
        columns=COLUMN_MAPPING
    )


    print("IO 4 PLAYER", flush=True)

    if "player" in df.columns:

        df.loc[:, "player"] = (
            df["player"]
            .astype(str)
            .str.strip()
            .str.replace("\n", "", regex=False)
        )


    print("IO 5 NUMERIC", flush=True)

    numeric_cols = [
        "player_id",
        "day",
        "duration",
        "rpe"
    ]


    for col in numeric_cols:

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
    print(df.columns.tolist(), flush=True)


    if "date" not in df.columns and "day" in df.columns:

        print("LOAD 4 DATE BUILD", flush=True)

        # Crear fecha sin pd.to_datetime
        df.loc[:, "date"] = (
            "2026-07-"
            + df["day"]
            .fillna(1)
            .astype(int)
            .astype(str)
            .str.zfill(2)
        )

        print("DATE STRING OK", flush=True)


    print("LOAD 5 RETURN", flush=True)

    return df