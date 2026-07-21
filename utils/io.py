import pandas as pd


COLUMN_MAPPING = {

    # Fecha
    "DÍA": "day",
    "DIA": "day",
    "FECHA": "date",
    "Fecha": "date",

    # Jugador
    "JUGADOR": "player",
    "Jugador": "player",

    # ID jugador
    "ID_JUGADOR": "player_id",
    "ID Jugador": "player_id",
    "id jugador": "player_id",

    # Duración
    "DURACIÓN": "duration",
    "Duración": "duration",
    "Duracion": "duration",

    # RPE
    "RPE": "rpe"

}



def normalize_columns(df):

    """
    Normaliza nombres y tipos de datos.
    """

    df = df.copy()


    # limpiar nombres columnas
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )


    df.rename(
        columns=COLUMN_MAPPING,
        inplace=True
    )


    # limpiar nombres jugadores
    if "player" in df.columns:

        df["player"] = (
            df["player"]
            .astype(str)
            .str.strip()
            .str.replace("\n", "", regex=False)
        )


    # convertir variables numéricas
    numeric_cols = [
        "player_id",
        "day",
        "duration",
        "rpe"
    ]


    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )


    return df


def normalize_training_columns(df):

    df = normalize_columns(df)

    if "date" not in df.columns:

        if (
            "day" in df.columns
            and "month" in df.columns
        ):

            month_map = {
                "Enero":1,
                "Febrero":2,
                "Marzo":3,
                "Abril":4,
                "Mayo":5,
                "Junio":6,
                "Julio":7,
                "Agosto":8,
                "Septiembre":9,
                "Octubre":10,
                "Noviembre":11,
                "Diciembre":12
            }


            df["month_num"] = (
                df["month"]
                .astype(str)
                .str.strip()
                .map(month_map)
            )


            df["date"] = pd.to_datetime(
                {
                    "year":2026,
                    "month":df["month_num"],
                    "day":df["day"]
                },
                errors="coerce"
            )

    else:

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )


    return df


def load_excel_monthly(path):

    """
    Lee Excel con una o varias hojas.
    Cada hoja puede ser un mes.
    """

    excel = pd.ExcelFile(path)

    frames = []


    month_map = {

        "Enero":1,
        "Febrero":2,
        "Marzo":3,
        "Abril":4,
        "Mayo":5,
        "Junio":6,
        "Julio":7,
        "Agosto":8,
        "Septiembre":9,
        "Octubre":10,
        "Noviembre":11,
        "Diciembre":12

    }


    for sheet in excel.sheet_names:

        df_month = pd.read_excel(
            path,
            sheet_name=sheet
        )


        df_month["month"] = sheet


        df_month = normalize_columns(
            df_month
        )


        # Crear fecha desde día + hoja

        if "day" in df_month.columns:

            month_number = month_map.get(
                sheet.strip(),
                7
            )


            df_month["date"] = pd.to_datetime(

                {
                    "year": 2026,
                    "month": month_number,
                    "day": df_month["day"]
                },

                errors="coerce"

            )


        frames.append(
            df_month
        )


    df = pd.concat(
        frames,
        ignore_index=True
    )


    return df

def load_uploaded_training_data(df):

    """
    Procesa datos provenientes
    de Import Data.
    """

    df = normalize_training_columns(
        df
    )


    required = [
        "player",
        "date",
        "duration",
        "rpe"
    ]


    missing = [
        c for c in required
        if c not in df.columns
    ]


    if missing:

        raise ValueError(
            f"Faltan columnas necesarias: {missing}"
        )


    return df



def load_training_data(path: str):

    """
    Carga dataset inicial AthleteOS.
    """

    df = load_excel_monthly(path)


    required = [
        "player",
        "date",
        "duration",
        "rpe"
    ]


    missing = [
        c for c in required
        if c not in df.columns
    ]


    if missing:

        raise ValueError(
            f"Faltan columnas necesarias: {missing}"
        )


    df = df.dropna(
        subset=[
            "player",
            "date"
        ]
    )


    return df