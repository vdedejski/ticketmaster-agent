from langchain.tools import tool

from src.repository.ticketmaster.events import get_ticketmaster_events

@tool("get_events")
def get_events(
    number_of_events=5,
    postal_code=None,
    start_datetime=None,
    end_datetime=None,
    city=None,
    country_code=None,
    state_code=None
) -> str:
    """Use this tool to retrieve events and details about them."""

    response = get_ticketmaster_events(
        number_of_events=number_of_events,
        postal_code=postal_code,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        city=city,
        country_code=country_code,
        state_code=state_code
    )

    return response

tools = [get_events]