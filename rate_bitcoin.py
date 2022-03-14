import requests
from datetime import datetime, timedelta

from my_eception import SendShitException

DATA_FORMAT = '%Y-%m-%d'
START_DATE_LIFE_BIT = "2015-01-01"
QUERY = ' https://api.coinbase.com/v2/prices/spot?currency=USD'
TYPE_TIMEDELTA = {
    'now': timedelta(days=0),
    'yesterday': timedelta(days=1),
    'week ago': timedelta(days=7),
    'month ago': timedelta(days=31),
    'year ago': timedelta(days=365),
}


def get_rate_bitcoin_for_button(message):
    current_date = datetime.now()

    timedelta_selected = TYPE_TIMEDELTA.get(message, None)
    if timedelta_selected is None:
        raise SendShitException("Send shit")

    parameter_query = f'&date={(current_date - timedelta_selected).strftime(DATA_FORMAT)}' if timedelta_selected else ''
    rate_bit = request_get_rate_bitcoin(parameter_query)

    return rate_bit


def get_rate_bitcoin_for_calendar(message):
    now_data = datetime.now().strftime(DATA_FORMAT)
    if START_DATE_LIFE_BIT > message or message > now_data:
        raise SendShitException("Send shit")

    parameter_query = f'&date={message}'
    rate_bit = request_get_rate_bitcoin(parameter_query)
    return rate_bit


def request_get_rate_bitcoin(parameters_query):
    bitcoin_api_url = f'{QUERY}{parameters_query}'
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    return response_json.get('data', {}).get('amount', 0)
