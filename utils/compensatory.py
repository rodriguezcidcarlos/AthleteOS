import pandas as pd

from utils.match_detection import is_match_day


def calculate_md1_work(minutes, status):

    if minutes >= 70:
        return 0, "Recuperación"

    elif 45 <= minutes < 70:

        if status == "Óptimo":
            return 20, "Trabajo aeróbico suave"

        elif status == "Subentrenamiento":
            return 30, "Trabajo aeróbico + fuerza"

        elif status == "Sobrecarga":
            return 10, "Movilidad + recuperación"


    elif 20 <= minutes < 45:

        if status == "Óptimo":
            return 35, "Trabajo aeróbico"

        elif status == "Subentrenamiento":
            return 45, "Trabajo físico completo"

        elif status == "Sobrecarga":
            return 20, "Trabajo compensatorio reducido"


    else:

        if status == "Óptimo":
            return 45, "Trabajo físico completo"

        elif status == "Subentrenamiento":
            return 55, "Trabajo físico completo"

        elif status == "Sobrecarga":
            return 30, "Trabajo aeróbico + fuerza"

    return 0, "-"



def calculate_compensatory(df):

    if not is_match_day(df):
        return None


    match_date = df["date"].max()

    match = (
        df[df["date"] == match_date]
        .copy()
    )


    rows = []


    for _, row in match.iterrows():

        player = row["player"]

        minutes = row["duration"]

        acwr = row["acwr"]


        # Estado ACWR
        if acwr < 0.80:

            status = "Subentrenamiento"

        elif acwr <= 1.30:

            status = "Óptimo"

        else:

            status = "Sobrecarga"


        md1_minutes, work = calculate_md1_work(
            minutes,
            status
        )


        rows.append({

            "player": player,

            "minutes_played": round(minutes),

            "acwr": round(acwr, 2),

            "status": status,

            "md1_minutes": md1_minutes,

            "compensatory_work": work

        })


    return pd.DataFrame(rows)