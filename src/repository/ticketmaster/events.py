from src.settings import settings
from src.repository.ticketmaster.common import TICKETMASTER_API_URL
import requests

def _format_embedded_events(events):
    """
    Formats a list of event data from Ticketmaster API response into a standardized dictionary format.

    Args:
        events (dict): The raw event data obtained from the Ticketmaster API.

    Returns:
        List[dict]: A list of dictionaries where each dictionary represents an event with relevant details.

    The function extracts and formats the following fields for each event:
        - Event name
        - URL for the event
        - Start and end dates of public ticket sales
        - Genre of the event
        - Main promoter's name
        - Additional information about the event
        - Any notes related to the event
        - Currency and price range for tickets
        - Venue name where the event will take place
    """
    found_events = []
    if events:
        for event in events.get('_embedded', {}).get('events', []):
            found_events.append({
                "event_name": event.get('name'),
                "url": event.get('url'),
                "public_ticket_sale_start": event.get('sales', {}).get('public', {}).get('startDateTime'),
                "public_ticket_sale_end": event.get('sales', {}).get('public', {}).get('endDateTime'),
                "genre": event.get('classifications', [{}])[0].get('genre', {}).get('name'),
                "main_promoter": event.get('promoter', {}).get('name'),
                "info": event.get('info'),
                "please_note": event.get('pleaseNote'),
                "currency": event.get('priceRanges', [{}])[0].get('currency'),
                "ticket_price_min": event.get('priceRanges', [{}])[0].get('min'),
                "ticket_price_max": event.get('priceRanges', [{}])[0].get('max'),
                "venue": event.get('_embedded', {}).get('venues', [{}])[0].get('name')
            })

    return found_events


def get_ticketmaster_events(
    number_of_events=5,
    postal_code=None,
    start_datetime=None,
    end_datetime=None,
    city=None,
    country_code=None,
    state_code=None
):
    """
    Fetches events from the Ticketmaster API based on the provided search parameters and formats the results.

    Args:
        size (int): The number of events to return (default is 5).
        postal_code (str, optional): The postal code to filter events by location.
        start_datetime (str, optional): The start date and time for filtering events.
        end_datetime (str, optional): The end date and time for filtering events.
        city (str, optional): The city to filter events by location.
        country_code (str, optional): The country code to filter events by location.
        state_code (str, optional): The state code to filter events by location.

    Returns:
        List[dict]: A list of formatted event dictionaries.

    The function constructs a query with the provided parameters and sends a GET request to the Ticketmaster API. 
    If the request is successful, it formats the response data using the _format_embedded_events function. 
    Any HTTP errors or general exceptions are caught and printed.
    """
    params = {
        'size': number_of_events,
        'apikey': settings.ticketmaster_consumer_key,
        'postalCode': postal_code,
        'startDateTime': start_datetime,
        'endDateTime': end_datetime,
        'city': city,
        'countryCode': country_code,
        'stateCode': state_code,
    }

    try:
        response = requests.get(TICKETMASTER_API_URL, params=params)
        response.raise_for_status()
        json_data = response.json()
        return _format_embedded_events(json_data)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
