import pandas as pd


def calculate_operational_status(acwr):

    if pd.isna(acwr):
        return "Sin datos"


    if acwr < 0.80:

        return "Subentrenamiento"


    elif acwr < 1.30:

        return "Óptimo"


    elif acwr < 1.50:

        return "Precaución"


    else:

        return "Riesgo elevado"



def calculate_status_column(df):

    df = df.copy()


    df["status"] = (
        df["acwr"]
        .apply(
            calculate_operational_status
        )
    )


    return df