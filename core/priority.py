import pandas as pd


def generate_intervention_list(squad: pd.DataFrame):

    squad = squad.copy()

    def calculate_priority(row):

        status = row["status"]

        risk_level = (
            row["risk"]["level"]
            if isinstance(row["risk"], dict)
            else None
        )

        if risk_level == "Alto":
            return "Alta"

        elif status in [
            "Precaución",
            "Subentrenamiento"
        ]:
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


    return (
        squad
        .sort_values("priority_order")
        .drop(columns=["priority_order"])
        .reset_index(drop=True)
    )