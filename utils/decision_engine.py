import pandas as pd
from settings.thresholds import ACWR_LIMITS

def analyze_player(player_df: pd.DataFrame):

    player_df = (
        player_df
        .sort_values("date")
        .reset_index(drop=True)
    )

    last = player_df.iloc[-1]

    result = {

        "status": evaluate_status(last),

        "alerts": evaluate_alerts(last),

        "recommendation": generate_recommendation(last),

    }

    return result



def evaluate_status(last):

    acwr = float(last["acwr"])

    if acwr < ACWR_LIMITS["undertraining"]:
        return "Subentrenamiento"

    elif acwr > ACWR_LIMITS["danger"]:
        return "Riesgo elevado"

    elif acwr > ACWR_LIMITS["optimal"]:
        return "Precaución"

    else:
        return "Óptimo"




def evaluate_alerts(last):

    alerts = []

    acwr = last["acwr"]


    if acwr < ACWR_LIMITS["undertraining"]:

        alerts.append(
            "Subentrenamiento: ACWR inferior al rango recomendado."
        )


    elif acwr > ACWR_LIMITS["danger"]:

        alerts.append(
            "ACWR en zona de riesgo elevado."
        )


    elif acwr > ACWR_LIMITS["optimal"]:

        alerts.append(
            "ACWR en zona de precaución."
        )


    if last["daily_load"] == 0:

        alerts.append(
            "Última sesión sin carga registrada."
        )


    return alerts



def generate_recommendation(last):

    acwr = float(last["acwr"])

    if acwr < ACWR_LIMITS["undertraining"]:

        return (
            "Incrementar progresivamente la carga "
            "controlando la respuesta aguda."
        )


    elif acwr > ACWR_LIMITS["danger"]:

        return (
            "Reducir la carga y valorar recuperación."
        )


    elif acwr > ACWR_LIMITS["optimal"]:

        return (
            "Monitorizar la evolución del jugador "
            "y ajustar la carga si es necesario."
        )


    else:

        return (
            "Mantener la planificación actual."
        )


def analyze_squad(df):

    results = []


    for player_id, player_df in df.groupby("player_id"):


        analysis = analyze_player(player_df)

        last = player_df.iloc[-1]


        results.append({

            "player_id": player_id,

            "player": last["player"],

            "daily_load": int(last["daily_load"]),

            "acwr": round(
                last["acwr"],
                2
            ),

            "status": analysis["status"],

            "alerts": analysis["alerts"],

            "recommendation": analysis["recommendation"]

        })


    return pd.DataFrame(results)