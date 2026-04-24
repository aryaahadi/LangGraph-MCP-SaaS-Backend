users = {
    "100": {
        "name": "Alice Corp",
        "email": "admin@alicecorp.com",
        "plan": "pro",
        "seats": 15,
        "seats_used": 12
    },
    "200": {
        "name": "DevFactory",
        "email": "it@devfactory.com",
        "plan": "free",
        "seats": 3,
        "seats_used": 3
    }
}

def get_user(user_id: str):
    return users.get(user_id)
