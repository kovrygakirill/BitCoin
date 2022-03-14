from datetime import datetime

from rate_bitcoin import DATA_FORMAT


def check_valid_for_calendar(msg):
    result = True

    try:
        if not datetime.strptime(msg or "", DATA_FORMAT):
            result = False
    except Exception:
        result = False

    return result
