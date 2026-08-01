import pandas as pd
from utils.validation import validate_training_data

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

MONTH_MAPPING = {
    "julio": (2026, 7),
    "agosto": (2026, 8),
    "septiembre": (2026, 9),
    "octubre": (2026, 10),
    "noviembre": (2026, 11),
    "diciembre": (2026, 12),
    "enero": (2027, 1),
    "febrero": (2027, 2),
    "marzo": (2027, 3),
    "abril": (2027, 4),
    "mayo": (2027, 5),
    "junio": (2027, 6),
}

def normalize_month_name(sheet_name):

    return (
        str(sheet_name)
        .strip()
        .lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )


def load_training_data(path):

    excel = pd.ExcelFile(path)

    dfs = []


    for sheet in excel.sheet_names:

        sheet_clean = normalize_month_name(sheet)

        if sheet_clean not in MONTH_MAPPING:
            continue

        temp = pd.read_excel(
            excel,
            sheet_name=sheet
        )

        if temp.empty:
                    continue

        temp["season_month"] = sheet_clean

        dfs.append(temp)


    if len(dfs) == 0:

        raise ValueError(
            "No se encontraron hojas válidas. "
            "El Excel debe contener una hoja por mes "
            "(Julio, Agosto, Septiembre...)."
        )
    

    df = pd.concat(
        dfs,
        ignore_index=True
    )


    df = normalize_columns(df)


    if "date" not in df.columns and "day" in df.columns:


        def build_date(row):

            year, month = MONTH_MAPPING[
                row["season_month"]
            ]

            try:

                return pd.Timestamp(
                    year=year,
                    month=month,
                    day=int(row["day"])
                )

            except Exception:

                return pd.NaT
        df["date"] = df.apply(
            build_date,
            axis=1
        )

    # Ordenar cronológicamente
    if {"player_id", "date"}.issubset(df.columns):

        df = df.sort_values(
            ["player_id", "date"]
        ).reset_index(
            drop=True
        )

    validate_training_data(df)

    return df