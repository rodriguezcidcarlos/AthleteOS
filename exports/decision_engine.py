    
def build_decision_engine(df, squad):

    latest = (
        df.sort_values("date")
          .groupby("player_id")
          .tail(1)
    )

    availability = (
        squad["risk"]
        .apply(
            lambda r: r.get("available", False)
        )
        .mean() * 100
    )

    acwr = latest["acwr"].mean()

    exposure = (
        (latest["acwr"] > 1.30)
        .mean() * 100
    )

    high_risk = (
        squad["risk"]
        .apply(
            lambda r: r["level"] == "Alto"
        )
        .sum()
    )

    # ==========================
    # Decisión
    # ==========================

    if (
        availability >= 90
        and 0.80 <= acwr <= 1.30
        and exposure < 10
        and high_risk == 0
    ):

        return {
            "status": "READY TO TRAIN",
            "color": "#22C55E",
            "summary": (
                "La plantilla presenta un estado óptimo para afrontar el siguiente microciclo."
            ),
            "recommendation": (
                "Mantener la planificación prevista."
            )
        }

    elif (
        availability >= 80
        and exposure < 25
    ):

        return {
            "status": "LOAD ADJUSTMENT RECOMMENDED",
            "color": "#F59E0B",
            "summary": (
                "Se observan indicadores que aconsejan ajustar parcialmente la carga."
            ),
            "recommendation": (
                "Reducir el volumen de alta intensidad en los jugadores más expuestos."
            )
        }

    return {
        "status": "HIGH RISK MICROCYCLE",
        "color": "#DC2626",
        "summary": (
            "La carga acumulada y la disponibilidad aconsejan modificar el microciclo."
        ),
        "recommendation": (
            "Revisar la planificación antes de la próxima sesión."
        )
    }