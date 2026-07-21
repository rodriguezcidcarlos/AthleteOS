import pandas as pd
from core.analytics import calculate_load_trend


class RiskEngine:


    def __init__(self):

        self.available = True



    def predict(self, player_df):

        player_df = (
            player_df
            .sort_values("date")
            .reset_index(drop=True)
        )

        last = player_df.iloc[-1]

        acwr = float(last["acwr"])

        trend = calculate_load_trend(player_df)

        score = 0
        drivers = []

        if acwr >= 1.5:

            score += 0.4

            drivers.append(
                "ACWR elevado respecto al rango objetivo"
            )


        elif acwr >= 1.3:

            score += 0.2

            drivers.append(
                "Incremento reciente de carga"
            )


        elif acwr < 0.8:

            score += 0.1

            drivers.append(
                f"ACWR bajo ({acwr:.2f}): exposición inferior al rango recomendado"
            )


        load_index = trend["load_index"]


        if load_index >= 1.5:

            score += 0.4

            drivers.append(
                f"Carga muy superior a la habitual ({load_index:.2f}×)"
            )


        elif load_index >= 1.2:

            score += 0.2

            drivers.append(
                f"Incremento moderado de carga ({load_index:.2f}×)"
            )


        if score >= 0.6:

            level = "Alto"


        elif score >= 0.3:

            level = "Medio"


        else:

            level = "Bajo"


        return {

            "available": True,

            "score": round(score, 2),

            "level": level,

            "load_index": round(load_index, 2),

            "drivers": drivers

        }