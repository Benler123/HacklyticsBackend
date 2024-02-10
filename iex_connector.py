import requests

api_token = "pk_6dcff48d8ea347d8aaafcbc3c123073e"

def get_stock_quote(ticker):
    ticker_quote_json = requests.get(f"https://api.iex.cloud/v1/data/CORE/QUOTE/{ticker}?token={api_token}").json()
    return ticker_quote_json[0]["peRatio"]

def get_all_tickers():
    url = f'https://cloud.iexapis.com/stable/ref-data/symbols?token={api_token}'
    all_ref_data = requests.get(url).json()
    us_exchanges = ["XNAS"]
    tickers = [symbol['symbol'] for symbol in all_ref_data if symbol['type'] == 'cs' and symbol['exchange'] in us_exchanges]
    return tickers
