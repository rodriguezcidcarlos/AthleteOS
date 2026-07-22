from dash import html, dcc
import dash_bootstrap_components as dbc

PASSWORD = "AthleteOS2026"


def login_layout():

    return dbc.Container(

        [

            html.Br(),
            html.Br(),

            dbc.Row(

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H2(
                                    "AthleteOS",
                                    className="text-center mb-4"
                                ),

                                dbc.Input(
                                    id="password-input",
                                    type="password",
                                    placeholder="Contraseña"
                                ),

                                html.Br(),

                                dbc.Button(
                                    "Acceder",
                                    id="login-button",
                                    color="primary",
                                    className="w-100"
                                ),

                                html.Br(),
                                html.Br(),

                                html.Div(
                                    id="login-message",
                                    className="text-danger text-center"
                                )

                            ]

                        )

                    ),

                    width=4

                ),

                justify="center"

            )

        ],

        fluid=True

    )