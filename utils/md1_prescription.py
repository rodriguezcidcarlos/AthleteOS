def build_md1_prescription(row):

    minutes = row["minutes_played"]
    acwr = row["acwr"]

    # Titulares
    if minutes >= 70:

        if acwr > 1.30:
            return (
                "Recuperación",
                "Bicicleta 20' + movilidad + fisioterapia"
            )

        elif acwr < 0.80:
            return (
                "Recuperación activa",
                "Movilidad + carrera continua 15'"
            )

        else:
            return (
                "Recuperación estándar",
                "Bicicleta 20' + fuerza preventiva"
            )

    # 40-69 minutos
    elif minutes >= 40:

        return (
            "Compensatorio medio",
            "Posesión 20' + 6×30 m sprint + fuerza"
        )

    # 20-39 minutos
    elif minutes >= 20:

        return (
            "Compensatorio alto",
            "HIIT 15×15 + juego reducido + fuerza"
        )

    # <20 minutos
    else:

        return (
            "Compensatorio completo",
            "Calentamiento + SSG + sprint + fuerza + vuelta a la calma"
        )