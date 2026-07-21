import pandas as pd
import numpy as np


# ==========================
# Configuración
# ==========================

np.random.seed(42)


players = [
    "Carlos",
    "Jugador_02",
    "Jugador_03",
    "Jugador_04",
    "Jugador_05",
    "Jugador_06",
    "Jugador_07",
    "Jugador_08",
    "Jugador_09",
    "Jugador_10",
    "Jugador_11",
    "Jugador_12",
    "Jugador_13",
    "Jugador_14",
    "Jugador_15",
    "Jugador_16",
    "Jugador_17",
    "Jugador_18",
    "Jugador_19",
    "Jugador_20",
    "Jugador_21",
    "Jugador_22",
    "Jugador_23",
    "Jugador_24",
    "Jugador_25",
]


days = 60


rows = []


# ==========================
# Generación entrenamiento
# ==========================

for player_id, player in enumerate(players, start=1):

    # perfil individual de carga

    base_duration = np.random.randint(
        50,
        90
    )

    base_rpe = np.random.randint(
        5,
        8
    )


    for day in range(1, days + 1):


        # días de descanso

        if np.random.random() < 0.15:

            duration = 0
            rpe = 0


        else:


            duration = max(
                20,
                int(
                    np.random.normal(
                        base_duration,
                        15
                    )
                )
            )


            rpe = int(
                np.clip(
                    np.random.normal(
                        base_rpe,
                        1.5
                    ),
                    3,
                    10
                )
            )


        rows.append(

            {

                "ID_JUGADOR": player_id,

                "DÍA": day,

                "JUGADOR": player,

                "DURACIÓN": duration,

                "RPE": rpe

            }

        )


# ==========================
# DataFrame
# ==========================

df = pd.DataFrame(rows)


# ordenar

df = df.sort_values(
    [
        "ID_JUGADOR",
        "DÍA"
    ]
)


# ==========================
# Exportar
# ==========================

output = "synthetic_training.xlsx"


df.to_excel(
    output,
    index=False
)


print(
    "Archivo generado:",
    df.shape
)

print(
    df.head(10)
)