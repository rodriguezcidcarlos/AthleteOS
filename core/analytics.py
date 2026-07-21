import pandas as pd


def calculate_load_trend(player_df):

    player_df = player_df.sort_values("date")

    loads = (
        player_df["daily_load"]
        .dropna()
    )

    # Excluir días sin entrenamiento
    loads = loads[loads > 0]

    if len(loads) < 5:

        return {

            "trend": "→ Estable",

            "change": 1.0,

            "load_index": 1.0

        }

    current = loads.iloc[-1]

    baseline = (
        loads
        .iloc[-5:-1]
        .mean()
    )

    if baseline == 0:

        load_index = 1.0

    else:

        load_index = current / baseline


    if load_index > 1.20:

        trend = "↑ Incrementando"

    elif load_index < 0.80:

        trend = "↓ Reduciendo"

    else:

        trend = "→ Estable"


    return {

        "trend": trend,

        # Compatibilidad con el código existente
        "change": round(load_index, 2),

        # Nuevo nombre recomendado
        "load_index": round(load_index, 2)

    }