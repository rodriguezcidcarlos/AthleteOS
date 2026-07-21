import pandas as pd


def generate_intervention_list(squad: pd.DataFrame):

    squad = squad.copy()


    def calculate_priority(row):

        status = row["status"]

        if status == "Riesgo elevado":
            return "Alta"

        elif status == "Precaución":
            return "Media"

        elif status == "Subentrenamiento":
            return "Media"

        else:
            return "Baja"


    squad["priority"] = squad.apply(
        calculate_priority,
        axis=1
    )


    priority_order = {
        "Alta": 1,
        "Media": 2,
        "Baja": 3
    }


    squad["priority_order"] = (
        squad["priority"]
        .map(priority_order)
    )


    squad = (
        squad
        .sort_values("priority_order")
        .drop(columns=["priority_order"])
    )


    return squad