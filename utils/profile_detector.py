import pandas as pd


CAPABILITIES = {

    "core": {

        "required": [

            "player_id",
            "player",
            "date",
            "duration",
            "rpe",
            "daily_load",
            "acute_ewma",
            "chronic_ewma",
            "acwr"

        ]

    },


    "gps": {

        "metrics": [

            "total_distance",
            "hsr_distance",
            "sprint_distance",
            "accelerations",
            "decelerations",
            "player_load",
            "max_speed"

        ]

    },


    "wellness": {

        "metrics": [

            "fatigue",
            "sleep",
            "stress",
            "soreness",
            "mood"

        ]

    },


    "hrv": {

        "metrics": [

            "rmssd",
            "ln_rmssd"

        ]

    }

}


def detect_profile(df: pd.DataFrame):

    columns = set(df.columns)

    profile = {}

    # CORE

    required = set(CAPABILITIES["core"]["required"])

    profile["core"] = required.issubset(columns)

    # RESTO DE MÓDULOS

    for module in ["gps", "wellness", "hrv"]:

        metrics = CAPABILITIES[module]["metrics"]

        available = sorted(

            list(

                columns.intersection(metrics)

            )

        )

        profile[module] = {

            "available": len(available) > 0,

            "metrics": available

        }

    return profile