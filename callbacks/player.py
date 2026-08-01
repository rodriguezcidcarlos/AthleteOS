import pandas as pd

from dash import (
    Input,
    Output,
    State,
    ALL
)


def register_player_callbacks(app, df, default_player):
    # ==========================
    # Actualizar selector jugador
    # ==========================

    @app.callback(
        Output("player-selector", "value"),
        Input("selected-player", "data"),
        State("uploaded-data-store", "data")
    )
    def update_player_selector(player_id, store_data):

        if store_data is None:
            return default_player

        squad = pd.DataFrame(store_data["squad"])

        if player_id in squad["player_id"].values:
            return player_id

        return int(squad.iloc[0]["player_id"])


    # ==========================
    # Abrir jugador desde Action Center
    # ==========================

    @app.callback(
        Output("main-tabs", "active_tab"),
        Output("selected-player", "data"),
        Input(
            {
                "type": "player-action",
                "player_id": ALL
            },
            "n_clicks"
        ),
        State(
            {
                "type": "player-action",
                "player_id": ALL
            },
            "id"
        ),
        prevent_initial_call=True
    )
    def open_player_from_action_center(clicks, ids):

        for click, item in zip(clicks, ids):

            if click:

                return (
                    "player",
                    item["player_id"]
                )

        return (
            "actions",
            default_player
        )
