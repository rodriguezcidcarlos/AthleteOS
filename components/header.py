from dash import html
import dash_bootstrap_components as dbc


def build_header(last_update):

    return [

        dbc.Container(

            [

                # ==========================
                # FRANJA AZUL SUPERIOR
                # ==========================

                dbc.Row(

                    [

                        dbc.Col(

                            html.Img(

                                src="/assets/logo/athleteos_logo.png",

                                style={

                                    "height": "120px",
                                    "width": "auto",
                                    "display": "block",
                                    "marginLeft": "18px",

                                },

                            ),

                            width=9,

                            className="d-flex align-items-center",

                        ),

                        dbc.Col(

                            dbc.Card(

                                dbc.CardBody(

                                    [

                                        html.Div(

                                            "● Sistema online",

                                            style={

                                                "color": "#16C784",
                                                "fontSize": "14px",
                                                "fontWeight": "600",

                                            },

                                        ),

                                        html.Hr(className="my-2"),

                                        html.Small(

                                            "Administrador",

                                            className="text-light opacity-75",

                                        ),

                                        html.Div(

                                            id="current-user",

                                            className="fw-bold text-white mb-3",

                                        ),

                                        html.Small(

                                            "Última actualización",

                                            className="text-light opacity-75",

                                        ),

                                        html.Div(

                                            last_update,

                                            className="fw-bold text-white mt-1 mb-3",

                                        ),

                                        dbc.Button(

                                            "Cerrar sesión",

                                            id="logout-button",

                                            color="light",

                                            size="sm",

                                            className="w-100",

                                        ),

                                    ]

                                ),

                                style={

                                    "backgroundColor": "#232B3E",
                                    "border": "1px solid rgba(255,255,255,.08)",
                                    "borderRadius": "16px",

                                },

                            ),

                            width=3,

                        ),

                    ],

                    className="align-items-center",

                    style={

                        "padding": "22px 26px",

                        "background": "#020E2A",

                        "borderTopLeftRadius": "22px",

                        "borderTopRightRadius": "22px",

                    },

                ),

                # ==========================
                # LÍNEA NARANJA
                # ==========================

                html.Div(

                    style={

                        "height": "3px",

                        "background": "#FF6B00",

                    }

                ),

                # ==========================
                # FRANJA BLANCA INFERIOR
                # ==========================

                dbc.Row(

                    dbc.Col(

                        html.Div(

                            "Performance Intelligence Platform",

                            style={

                                "color": "#0B132B",
                                "fontSize": "15px",
                                "fontWeight": "500",
                                "letterSpacing": "3px",
                                "marginLeft": "18px",

                            },

                        ),

                        width=12,

                    ),

                    style={

                        "padding": "14px 28px",

                        "background": "#FFFFFF",

                        "borderBottomLeftRadius": "22px",

                        "borderBottomRightRadius": "22px",

                    },

                ),

            ],

            fluid=True,

            style={

                "marginTop": "18px",
                "marginBottom": "20px",
                "padding": "0",
                "overflow": "hidden",
                "borderRadius": "22px",
                "boxShadow": "0 12px 30px rgba(0,0,0,.15)",

            },

        )

    ]