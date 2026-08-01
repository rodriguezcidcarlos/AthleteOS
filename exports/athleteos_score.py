def calculate_athleteos_score(df, squad):

    # ==========================
    # Disponibilidad
    # ==========================

    availability = (
        squad["risk"]
        .apply(
            lambda x: isinstance(x, dict)
            and x.get("available", False)
        )
        .mean() * 100
    )

    availability_score = availability

    # ==========================
    # Último estado por jugador
    # ==========================

    latest = (
        df.sort_values("date")
          .groupby("player_id")
          .tail(1)
    )

    # ==========================
    # ACWR
    # ==========================

    acwr = latest["acwr"].mean()

    if 0.80 <= acwr <= 1.30:
        acwr_score = 100

    elif 0.70 <= acwr < 0.80:
        acwr_score = 80

    elif 1.30 < acwr <= 1.50:
        acwr_score = 70

    else:
        acwr_score = 40

    # ==========================
    # Exposición
    # ==========================

    exposure = (
        (latest["acwr"] > 1.30)
        .mean() * 100
    )

    exposure_score = max(
        0,
        100 - exposure
    )

    # ==========================
    # Riesgo predictivo
    # ==========================

    high_risk = (
        squad["risk"]
        .apply(
            lambda r: r["level"] == "Alto"
        )
        .mean() * 100
    )

    risk_score = max(
        0,
        100 - high_risk
    )

    # ==========================
    # Score final
    # ==========================

    score = (

        availability_score * 0.35 +

        acwr_score * 0.25 +

        exposure_score * 0.20 +

        risk_score * 0.20

    )


    return {

        "score": round(score, 1),

        "availability": round(availability, 1),

        "acwr": round(acwr, 2),

        "exposure": round(exposure, 1),

        "risk": round(high_risk, 1)

    }