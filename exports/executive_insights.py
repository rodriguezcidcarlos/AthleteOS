def generate_executive_insights(df, squad):

    insights = []

    # ==========================
    # Disponibilidad
    # ==========================

    availability = round(
        squad["risk"]
        .apply(
            lambda x: isinstance(x, dict)
            and x.get("available", False)
        )
        .mean() * 100,
        1
    )

    if availability >= 90:

        insights.append(
            "La disponibilidad de la plantilla es muy elevada, lo que permite mantener la planificación prevista."
        )

    elif availability >= 80:

        insights.append(
            "La disponibilidad es adecuada para afrontar el microciclo con normalidad."
        )

    elif availability >= 70:

        insights.append(
            "La disponibilidad comienza a reducirse. Conviene monitorizar la evolución de los jugadores con mayor carga."
        )

    else:

        insights.append(
            "La disponibilidad es baja. Se recomienda revisar la planificación del entrenamiento."
        )

    # ==========================
    # ACWR colectivo
    # ==========================

    latest = (
        df.sort_values("date")
        .groupby("player_id")
        .tail(1)
    )

    acwr = round(
        latest["acwr"].mean(),
        2
    )

    if acwr < 0.80:

        insights.append(
            "La carga colectiva se sitúa por debajo del rango recomendado."
        )

    elif acwr <= 1.30:

        insights.append(
            "El ACWR medio de la plantilla se encuentra dentro del rango óptimo."
        )

    elif acwr <= 1.50:

        insights.append(
            "Se observa un incremento de la carga colectiva que requiere seguimiento."
        )

    else:

        insights.append(
            "La carga acumulada es elevada y aumenta el riesgo de sobrecarga."
        )

    # ==========================
    # Exposición elevada
    # ==========================

    high = int(
        (latest["acwr"] > 1.30).sum()
    )

    if high == 0:

        insights.append(
            "No se detectan jugadores con exposición elevada en la última evaluación."
        )

    elif high <= 2:

        insights.append(
            f"Se identifican {high} jugador(es) con exposición elevada que requieren seguimiento individual."
        )

    else:

        insights.append(
            f"Se identifican {high} jugadores con exposición elevada, por lo que se recomienda ajustar la carga de entrenamiento."
        )

    return insights