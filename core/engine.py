import pandas as pd

from core.load import (
    calculate_daily_load,
    calculate_acwr
)

from utils.decision_engine import (
    analyze_player as decision_engine_player
)

from core.analytics import calculate_load_trend
from core.priority import generate_intervention_list
from core.risk_engine import RiskEngine

class AthleteOSCore:


    def __init__(self):

        self.name = "AthleteOS Core"

        self.risk_engine = RiskEngine()

    def _build_risk_context(
        self,
        player_df,
        decision,
        trend
        ):


        risk = self.risk_engine.predict(player_df)


        risk["action"] = decision["recommendation"]


        if decision["status"] == "Subentrenamiento":

            risk["interpretation"] = (

                "El jugador presenta una exposición acumulada "
                "inferior al rango recomendado, con un incremento "
                "reciente de carga respecto a su patrón habitual. "
                "La progresión debe realizarse de forma controlada."

            )


        elif risk["level"] == "Alto":

            risk["interpretation"] = (

                "El jugador presenta indicadores compatibles con "
                "elevada exposición y requiere ajuste de carga."

            )


        else:

            risk["interpretation"] = (

                "La evolución de carga se encuentra dentro de los "
                "rangos esperados. Mantener seguimiento."

            )


        return risk


    def prepare_data(self, df):

        print("PREP 1 COPY", flush=True)

        df = df.copy()

        print("PREP 2 PLAYER ID", flush=True)

        if "player_id" in df.columns:
            df.loc[:, "player_id"] = pd.to_numeric(
                df["player_id"],
                errors="coerce"
            )

        print("PREP 3 NUMERIC", flush=True)

        for col in ["duration", "rpe"]:

            print("PREP CONVERT", col, flush=True)

            df.loc[:, col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        print("PREP 4 FILL NA", flush=True)

        df.loc[:, "duration"] = df["duration"].fillna(0)
        df.loc[:, "rpe"] = df["rpe"].fillna(0)

        print("PREP 5 DATE", flush=True)

        print(df["date"].head().to_string(), flush=True)
        print(df["date"].dtype, flush=True)

        print("PREP 5 DATE BEFORE RETURN", flush=True)

        return df
      
    squad = core.analyze_squad(df_core)

    print(squad.head())

    def analyze_player(self, player_df: pd.DataFrame):

        player_df = (
            player_df
            .sort_values("date")
            .reset_index(drop=True)
        )


        decision = decision_engine_player(player_df)

        trend = calculate_load_trend(player_df)

        last = player_df.iloc[-1]


        return {

            "player_id": int(last["player_id"]),

            "player": last["player"],

            "daily_load": (
                int(last["daily_load"])
                if pd.notna(last["daily_load"])
                else 0
            ),

            "acwr": (
                round(float(last["acwr"]),2)
                if pd.notna(last["acwr"])
                else None
            ),

            "status": decision["status"],

            "alerts": decision["alerts"],

            "recommendation": decision["recommendation"],

            "trend": trend["trend"],

            "change": float(trend["change"]),

            "load_index": float(trend["load_index"]),

            "risk": self._build_risk_context(
                player_df,
                decision,
                trend
            )

        }
    
    def analyze_squad(self, df: pd.DataFrame):

        results = []

        for player_id, player_df in df.groupby("player_id"):

            analysis = self.analyze_player(player_df)

            results.append(analysis)

        return pd.DataFrame(results)
    
    def prioritize_squad(self, squad_analysis):

        return generate_intervention_list(
            squad_analysis
        )