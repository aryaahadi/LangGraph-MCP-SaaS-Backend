def is_over_seat_limit(user):
    return user["seats_used"] > user["seats"]


def usage_summary(user):
    return {
        "plan": user["plan"],
        "seats_total": user["seats"],
        "seats_used": user["seats_used"],
        "over_limit": is_over_seat_limit(user)
    }
