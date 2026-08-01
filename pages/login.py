from dash import html
from dash import dcc

import dash_bootstrap_components as dbc


layout = dbc.Container(

    [

        dbc.Row(

            dbc.Col(

                dbc.Card(

                    [

                        dbc.CardBody(

                            [

                                html.H2(
                                    "AthleteOS",
                                    className="text-center text-primary mb-4"
                                ),

                                dbc.Input(
                                    id="login-username",
                                    placeholder="Usuario",
                                    type="text",
                                    className="mb-3"
                                ),

                                dbc.Input(
                                    id="login-password",
                                    placeholder="Contraseña",
                                    type="password",
                                    className="mb-3"
                                ),

                                dbc.Button(
                                    "Entrar",
                                    id="login-button",
                                    color="primary",
                                    className="w-100"
                                ),

                                html.Br(),

                                html.Div(
                                    id="login-message",
                                    className="text-danger mt-3 text-center"
                                ),

                                dcc.Location(
                                    id="login-redirect"
                                )

                            ]

                        )

                    ]

                ),

                width=4

            ),

            justify="center",
            className="vh-100 align-items-center"

        )

    ],

    fluid=True

)