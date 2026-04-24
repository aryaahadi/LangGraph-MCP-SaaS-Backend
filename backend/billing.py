def available_plans():
    return ["free", "starter", "pro", "enterprise"]


def change_plan(user, new_plan):
    if new_plan not in available_plans():
        return {"error": "invalid plan"}

    old = user["plan"]
    user["plan"] = new_plan

    return {
        "status": "ok",
        "old": old,
        "new": new_plan
    }
