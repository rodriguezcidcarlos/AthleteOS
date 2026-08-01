from datetime import datetime
import pandas as pd

from utils.io import load_training_data
from core.engine import AthleteOSCore


def initialize_data(data_file):

    df = load_training_data(data_file)

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    core = AthleteOSCore()

    df = core.prepare_data(df)

    squad = core.analyze_squad(df)

    priority = core.prioritize_squad(squad)

    players = (
        df[["player_id", "player"]]
        .drop_duplicates()
    )

    default_player = (
        players["player_id"].iloc[0]
        if not players.empty
        else None
    )

    last_update = datetime.now().strftime(
        "%d %b %Y · %H:%M"
    )

    return (
        df,
        squad,
        priority,
        default_player,
        last_update
    )