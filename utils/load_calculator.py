import pandas as pd


from settings.thresholds import (
    EWMA_ACUTE_SPAN,
    EWMA_CHRONIC_SPAN,
    ACWR_LIMITS
)


def calculate_daily_load(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["daily_load"] = df["duration"] * df["rpe"]

    return df


def calculate_ewma(series: pd.Series, span: int) -> pd.Series:

    return series.ewm(
        span=span,
        adjust=False
    ).mean()


def calculate_acwr(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df = df.sort_values(
        ["player_id", "date"]
    ).reset_index(drop=True)

    df["acute_ewma"] = (
        df.groupby("player_id")["daily_load"]
        .transform(lambda x: calculate_ewma(x, EWMA_ACUTE_SPAN))
    )

    df["chronic_ewma"] = (
        df.groupby("player_id")["daily_load"]
        .transform(lambda x: calculate_ewma(x, EWMA_CHRONIC_SPAN))
    )

    df["acwr"] = (
        df["acute_ewma"] /
        df["chronic_ewma"].replace(0, 0.01)
    )

    df["status"] = df["acwr"].apply(
        lambda x: calculate_status(x) if pd.notna(x) else "Sin datos"
    )

    return df


def calculate_status(acwr: float) -> str:

    if acwr < ACWR_LIMITS["undertraining"]:
        return "Subentrenamiento"

    elif acwr < ACWR_LIMITS["optimal"]:
        return "Óptimo"

    elif acwr < ACWR_LIMITS["danger"]:
        return "Precaución"

    return "Riesgo elevado"

def calculate_status_code(acwr):

    if acwr < 0.80:
        return 1

    elif acwr < 1.30:
        return 2

    elif acwr < 1.50:
        return 3

    return 4