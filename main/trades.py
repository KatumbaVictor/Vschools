API_KEY = ''
ACCOUNT_ID = ''
OANDA_URL = 'https://api-fxpractice.oanda.com'

SECURE_HEADER = {
	'Authorization': f'Bearer {API_KEY}',
	'Content-Type': 'application/json'
}

def get_candlestick_data(instrument, timeframe, count):
	url = f'{OANDA_URL}/v3/instruments/{instrument}/candles'
	params = {
		'count': count,
		'granularity':timeframe
	}

	response = requests.get(url, headers=headers, params=params)
	data = response.json()
	return data

def execute_trade(instrument, units, side):
	url = f'{OANDA_URL}/v3/accounts/{account_id}/orders'
	data = {
		'order':{
			'instrument':instrument,
			'units'
		}
	}