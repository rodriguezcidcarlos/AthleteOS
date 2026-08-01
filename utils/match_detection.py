MATCH_MINUTES = 80
MATCH_RPE = 7
MIN_STARTERS = 7

def is_match_day(session):

    starters = session[
        (session["duration"] >= MATCH_MINUTES) &
        (session["rpe"] >= MATCH_RPE)
    ]

    return len(starters) >= MIN_STARTERS