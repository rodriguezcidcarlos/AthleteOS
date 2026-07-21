import pandas as pd


def generate_intervention_list(squad: pd.DataFrame):

    squad = squad.copy()

    def calculate_priority(row):

        status = row["status"]

        risk_level = None

        if isinstance(row["risk"], dict):
            risk_level = row["risk"].get("level")


        if risk_level == "Alto":
            return "Alta"


        if status == "Precaución":
            return "Alta"


        if status == "Subentrenamiento":
            return "Media"


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


    squad.loc[:, "priority_order"] = (
        squad["priority"]
        .map(priority_order)
    )


    return (
        squad
        .sort_values("priority_order")
        .drop(columns=["priority_order"])
        .reset_index(drop=True)
    )