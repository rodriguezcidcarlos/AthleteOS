from dash import html
import dash_bootstrap_components as dbc


def build_executive_table(squad, df):

    rows = []
    
    MIN_BASELINE_SESSIONS = 6
    
    colors = {

        "Alto": "danger",
        "Medio": "warning",
        "Bajo": "success"

    }


    for _, player in squad.iterrows():

        player_id = player["player_id"]


        data = df[
            df["player_id"] == player_id
        ].sort_values(
            "date"
        )

        if len(data) == 0:
            continue
        
        # -------------------------
        # Estado actual
        # -------------------------

        last = data.iloc[-1]

        acwr = round(
            last["acwr"],
            2
        )


        load_7 = round(
            data.tail(7)["daily_load"].sum()
        )

        # -------------------------
        # Baseline individual
        # -------------------------

        has_baseline = (
            len(data) >= MIN_BASELINE_SESSIONS
        )


        variation_pct = None


        trend = "⚪"
        trend_text = "Sin baseline"


        reason = (
            f"Historial insuficiente "
            f"({len(data)}/{MIN_BASELINE_SESSIONS} sesiones) "
            "para evaluar desviaciones individuales."
        )


        # -------------------------
        # Tendencia ACWR ventana reciente
        # -------------------------

        if has_baseline:


            current_acwr = data.iloc[-1]["acwr"]


            previous_window = (
                data.iloc[-6:-1]["acwr"]
                .mean()
            )


            if previous_window > 0:


                variation = (
                    (current_acwr - previous_window)
                    /
                    previous_window
                )


                variation_pct = round(
                    variation * 100,
                    1
                )


                trend = "➡️"
                trend_text = "Estable"


                reason = (
                    "Exposición dentro del patrón habitual."
                )



                # -------------------------
                # Incremento con riesgo
                # -------------------------

                if (
                    variation >= 0.15 and current_acwr >= 1.30
                ):

                    trend = "🔴"
                    trend_text = "Pico de carga"


                # Incremento a vigilar

                elif variation >= 0.10:

                    trend = "📈"
                    trend_text = "Incremento relevante"


                # Descarga marcada

                elif variation <= -0.15:

                    trend = "🔵"
                    trend_text = "Descarga significativa"


                elif variation <= -0.10:

                    trend = "📉"
                    trend_text = "Descarga"



        status = player["risk"]["level"]


        # -------------------------
        # Motivo de alerta
        # -------------------------

        reason = "Exposición dentro del patrón habitual"


        if trend_text == "Pico de carga":

            reason = (
                f"Incremento relativo +{variation_pct}% "
                f"respecto a la ventana reciente "
                f"con ACWR elevado ({acwr})"
            )


        elif trend_text == "Incremento relevante":

            reason = (
                f"Aumento relativo de exposición "
                f"respecto a la tendencia reciente "
                f"(ACWR {acwr})"
            )


        elif trend_text == "Incremento relevante":

            reason = (
                f"Aumento relativo +{variation_pct}% "
                f"respecto a la tendencia reciente "
                f"(ACWR {acwr})"
            )


        elif trend_text == "Descarga significativa":

            reason = (
                f"Reducción relativa {variation_pct}% "
                f"respecto a la exposición reciente "
                f"(ACWR {acwr})"
            )

        elif trend_text == "Descarga":

            reason = (
                f"Disminución relativa {variation_pct}% "
                f"de exposición reciente "
                f"(ACWR {acwr})"
            )

        # -------------------------
        # Acción recomendada
        # -------------------------

        if trend_text == "Sin baseline":

            recommendation = (
                "Continuar monitorización. "
                "Necesarias más sesiones para establecer "
                "referencia individual."
            )


        elif trend_text == "Pico de carga":


            recommendation = (

                "Revisar planificación próxima. "
                "Valorar ajuste de volumen/intensidad "
                "según disponibilidad y calendario."

            )


        elif trend_text == "Incremento relevante":

            recommendation = (

                "Mantener planificación actual. "
                "Realizar seguimiento de respuesta individual."

            )


        elif trend_text == "Descarga significativa":

            recommendation = (

                "Confirmar si la descarga es intencionada. "
                "Controlar recuperación y disponibilidad."

            )


        elif trend_text == "Descarga":

            recommendation = (

                "Mantener control de recuperación."

            )


        else:

            recommendation = (

                player.get(
                    "recommendation",
                    "Mantener planificación actual."
                )

            )



        rows.append(

            html.Tr(

                [

                    html.Td(
                        player["player"]
                    ),


                    html.Td(

                        dbc.Badge(

                            status,

                            color=colors.get(
                                status,
                                "secondary"
                            )

                        )

                    ),


                    html.Td(
                        acwr
                    ),


                    html.Td(
                        load_7
                    ),


                    html.Td(

                        [
                            trend,
                            " ",
                            trend_text
                        ]

                    ),


                    html.Td(
                        reason
                    ),


                    html.Td(
                        recommendation
                    )

                ]

            )

        )



    return dbc.Table(

        [

            html.Thead(

                html.Tr(

                    [

                        html.Th("Jugador"),
                        html.Th("Estado"),
                        html.Th("ACWR"),
                        html.Th("Carga 7 días"),
                        html.Th("Tendencia"),
                        html.Th("Motivo de alerta"),
                        html.Th("Acción")

                    ]

                )

            ),


            html.Tbody(
                rows
            )

        ],


        bordered=True,

        hover=True,

        striped=True,

        responsive=True,

        className="shadow-sm"

    )