tickets = []
ticket_counter = 1

def create_ticket(user_id: str, title: str, body: str):
    global ticket_counter
    ticket = {
        "id": ticket_counter,
        "user_id": user_id,
        "title": title,
        "body": body,
        "status": "open"
    }
    tickets.append(ticket)
    ticket_counter += 1
    return ticket
