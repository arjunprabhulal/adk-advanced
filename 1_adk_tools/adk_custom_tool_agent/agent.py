from google.adk.agents import Agent
from google.adk.tools import FunctionTool

def get_order_status(order_id: str):
    """
    Retrieves the status of an order by order ID.

    Args:
        order_id (str): The unique order identifier.
    """

    return {"order_id": order_id, "status": "Shipped", "delivery_date": "Nov 24, 2025"}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="support_agent",
    instruction="You are a helpful customer support assistant.",
    tools=[FunctionTool(get_order_status)],

)

