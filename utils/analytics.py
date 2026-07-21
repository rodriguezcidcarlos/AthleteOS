import pandas as pd


def calculate_load_trend(player_df: pd.DataFrame):

    """
    Compara la carga reciente con la anterior.
    """

    if len(player_df) < 6:

        return {
            "trend": "Sin datos",
            "change": 0
        }

    recent = player_df.tail(3)["daily_load"].mean()

    previous = player_df.iloc[-6:-3]["daily_load"].mean()

    if previous == 0:

        change = 0

    else:

        change = ((recent - previous) / previous) * 100


    if change > 10:

        trend = "↑ Incrementando"

    elif change < -10:

        trend = "↓ Disminuyendo"

    else:

        trend = "→ Estable"


    return {
        "trend": trend,
        "change": float(round(change, 1))
    }