from datetime import datetime


def get_timestamp():
    now = datetime.now()
    dt = int(now.strftime("%d"))
    dt = (
        str(dt) + "th"
        if 11 <= dt <= 13
        else str(dt) + {1: "st", 2: "nd", 3: "rd"}.get(dt % 10, "th")
    )
    return "{0}, {1} {2}".format(
        now.strftime("%A"), dt, now.strftime("%B, %Y %I:%M:%S %p")
    )
