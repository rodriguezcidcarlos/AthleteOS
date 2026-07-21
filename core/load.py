import pandas as pd


from settings.thresholds import (
    EWMA_ACUTE_SPAN,
    EWMA_CHRONIC_SPAN,
    ACWR_LIMITS
)

from core.status_engine import calculate_status_column

def calculate_daily_load(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["duration"] = pd.to_numeric(
        df["duration"],
        errors="coerce"
    )

    df["rpe"] = pd.to_numeric(
        df["rpe"],
        errors="coerce"
    )


    df["daily_load"] = (
        df["duration"] *
        df["rpe"]
    )

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
        .transform(
            lambda x: calculate_ewma(
                x,
                EWMA_ACUTE_SPAN
            )
        )
    )


    df["chronic_ewma"] = (
        df.groupby("player_id")["daily_load"]
        .transform(
            lambda x: calculate_ewma(
                x,
                EWMA_CHRONIC_SPAN
            )
        )
    )


    df["acwr"] = (
        df["acute_ewma"] /
        df["chronic_ewma"].replace(0,0.01)
    )


    # Estado operativo único
    df = calculate_status_column(df)


    return df


