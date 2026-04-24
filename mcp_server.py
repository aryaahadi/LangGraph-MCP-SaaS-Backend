from mcp.server.fastmcp import FastMCP

from backend.users import get_user
from backend.billing import available_plans, change_plan
from backend.usage import usage_summary, is_over_seat_limit
from backend.tickets import create_ticket

mcp = FastMCP("saas-backend")


@mcp.tool()
def fetch_customer(user_id: str):
    user = get_user(user_id)
    if not user:
        return {"error": "not found"}
    return user


@mcp.tool()
def upgrade_plan(user_id: str, new_plan: str):
    user = get_user(user_id)
    if not user:
        return {"error": "not found"}

    return change_plan(user, new_plan)


@mcp.tool()
def check_usage(user_id: str):
    user = get_user(user_id)
    if not user:
        return {"error": "not found"}

    return usage_summary(user)


@mcp.tool()
def over_quota(user_id: str):
    user = get_user(user_id)
    if not user:
        return {"error": "not found"}

    return {"over_limit": is_over_seat_limit(user)}


@mcp.tool()
def open_ticket(user_id: str, title: str, body: str):
    return create_ticket(user_id, title, body)


@mcp.tool()
def list_plans():
    return available_plans()


if __name__ == "__main__":
    mcp.run()
